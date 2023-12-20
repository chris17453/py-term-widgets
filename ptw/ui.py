
from .io import io
import curses

from .utils import split_string_and_extract_colors

def clear_block(buffer, left,top, width, height,color):
    """Clear a block area on the screen."""
    block=" "*width
    try:
        for y in range(top, top + height):
    
            buffer.addstr(y, left,block,color)
    except curses.error:
        pass

class ui(io):

    def move_y(self,distance=None,position=None):
        """Main function responsible for cursor movment along the line axis"""
        #self.logger.warn(f"Move-Y: Y:{self.cursor_y} Position:{position} Distance:{distance} Top Line: {self.top_line}")
        if position!=None:
            if position<0:
                position=0
            if position>=len(self.lines)-1:
                position=len(self.lines)-1
            
            # if its within the curent window view.....
            elif position >=self.top_line and position <self.top_line+self.elements['text'].height:
                self.cursor_y=position-self.top_line
            else:
            # otherwise scroll
                self.top_line=position
                self.cursor_y=0
        elif distance!=None:
            if self.cursor_y+distance>self.elements['text'].height-1:

                # its below the viewport
                if self.top_line+self.elements['text'].height<self.last_screen_line+1:

                    self.top_line +=1
                    self.cursor_y=self.elements['text'].height-1
            
            elif self.cursor_y+distance<0:
                # It's above the view port
                self.cursor_y=0
                if self.top_line>0:
                    self.top_line +=distance
            else:
                # its in the middle of the viewport
                if self.lines[self.top_line+self.cursor_y+distance]['number']!=None:
                    self.cursor_y+=distance
   
    
    def move_x(self,distance=None,position=None):
        """Main function responsible for cursor movment along the colum axis"""
        if position!=None:
            self.cursor_x = position   
            self.target_cursor_x=self.cursor_x
        elif distance!=None:
            if distance<0:
                if self.cursor_x>=distance:
                    self.cursor_x +=distance
                    if self.cursor_x<0:
                        end=self.get_previous_line()
                        
                        if end is None or end['width']==None:
                            self.cursor_x=0
                        else:
                            line=self.get_line()
                            if line!=None and end['number']==line['number']:
                            # its the same line split. put it on the previous character
                                self.cursor_x=end['width']-1
                            else:
                            # put it on character past the end, its a different line
                                self.cursor_x=end['width']
                        self.move_y(distance=-1)

            elif distance>0:
                line=self.get_line()
                if self.cursor_x+distance<=line['width']: 
                    if self.cursor_x>=self.elements['text'].width-1:
                        self.cursor_x=0
                        self.logger.warn("Calc 1")
                        self.calculate_page()
                        self.move_y(distance=1)
                    else:
                        self.cursor_x +=distance    
                else:
                    if self.cursor_y+self.top_line<self.last_screen_line:
                        self.move_y(distance=1)
                        self.cursor_x=0
                    else:
                        pass
                    
        
            self.target_cursor_x=self.cursor_x


    
    def draw_border(self):
        """Draw a border arround our window"""
        self.draw_box(True)

    def display_text(self):
        """Blit formated text to screen"""
        wrapped_text = self.wrap_text()

        if self.active:
            color=self.colors['ACTIVE_TEXT']
        else:
            color=self.colors['INACTIVE_TEXT']

        clear_block(self.buffer,self.elements['text'].left, self.elements['text'].top, self.elements['text'].width,self.elements['text'].height,color)
        for idx in range(self.elements['text'].height):
            try:
                line=wrapped_text[self.top_line+idx]
                self.buffer.addstr(idx + self.elements['text'].top, 
                                self.elements['text'].left, 
                                line[:self.elements['text'].width],
                                color)  # Adjust for line numbers
            except Exception as ex:
                self.logger.error(f"Display Text : {ex}") 


    def calculate_page(self):
        """Builds a precomputed array with information for every line of text. This is the main data object"""
        try:
            self.lines=[]
            line=0
            screen_line=0
            index=0
            for i in range(max(len(self.text),len(self.text)+self.elements['text'].height)):
                if line<len(self.text):
                    #calc_text=split_string_and_extract_colors(self.text[line])
                    #text_length=0
                    #for item in calc_text:
                    #    if isinstance(item,str):
                    #        text_length+=len(item)
                    #
                    text_length=len(self.text[line])
                    text_left=0
                    if text_length==0:
                            self.lines.append({'start':0,'end':0,'number':line,'width':0,'display':line+1,'y':i,'line_start':screen_line,'line_end':screen_line,"zero":0,'index':index})
                            self.last_screen_line=screen_line
                            screen_line +=1
                            index+=1
                    lines=[]
                    screen_line_start=screen_line
                    while text_length>0:
                            text_right=min(text_length,self.elements['text'].width)+text_left
                            if text_left==0:
                                display=line+1
                            else:
                                display=''

                            width=text_right-text_left
                            lines.append({'start':text_left,'end':text_right,'number':line,'width':width,'display':display,'y':i,'line_start':screen_line_start,'mid':0,'index':index})
                            # if this is the line the cursor is on and we are at the end, insert a blank line
                            text_length -= self.elements['text'].width
                            
                            if text_length==0:
                                index +=1
                                screen_line +=1
                                lines.append({'start':text_right,'end':text_right,'number':line,'width':0,'display':'','y':i,'line_start':screen_line_start,'temp_line':0,'index':index})
                            text_left+=self.elements['text'].width
                            self.last_screen_line=screen_line
                            screen_line +=1
                            index+=1
                    for a in range(len(lines)):
                        lines[a]['line_end']=screen_line-1
                    self.last_line=line
                    line=line+1
                    self.lines+=lines

                else:
                    self.lines.append({'start':None,'end':None,'number':None,'width':0,'display':'~','y':i,'line_start':screen_line,'line_end':screen_line,'index':index})
                    index+=1
                    screen_line +=1
            #self.logger.warning(f"last {self.last_screen_line} {self.lines[self.last_screen_line]}")
            #self.save_to_json("debug.json",self.lines)
        except Exception as ex:
            self.logger.Error("Calculate page:"+ex)

    def display_line_numbers(self):
        """Creates the line number gutter"""
        line_range=self.elements['line_numbers'].height
        #self.logger.warn(f"Drawing Line Numbers {line_range}")
        
        for i in range(line_range):
            line_num = f"{self.lines[self.top_line+i]['display']} ".rjust(4)
            try:
                self.buffer.addstr(i + self.elements['line_numbers'].top, 
                                    self.elements['line_numbers'].left, 
                                    line_num, self.colors['LINE_NUMBERS'])
            except Exception as ex:
                self.logger.error(f"Line number : {ex}") 

    def display_info(self):
        """Display info at the bottom of the window, line position etc"""
        line_num=self.cursor_y+self.top_line
        line=self.lines[line_num]
        if line['number']!=None:
            end_line=self.lines[line_num]['line_end']
            end_line_pos=self.lines[end_line]['end']
            x_pos=line['start']+self.cursor_x
            line_info=f" Line: {line['number']+1} Pos:{x_pos+1} of {end_line_pos+1}"
        else:
            line_info=""

        info = f"X: {self.cursor_x+1}, Y: {self.cursor_y+1} /"+line_info
        self.buffer.addstr(self.elements['info'].top, 
                           self.elements['info'].left, 
                           info[:self.max_x - 2],
                           self.colors['INFO'])
        
    def wrap_text(self):
        """Create a word wrapped set of text based of internal text array"""
        wrapped_lines = []
        for line in self.lines:
            if line['number']==None:
                wrapped_lines.append('')
            else:
                wrapped_lines.append(self.text[line['number']][line['start']:line['end']])
        return wrapped_lines

    def adjust_cursor(self):
        """ Adjust cursor_x to the end of the line if it's longer than the line length """
        pass
        #line=self.lines[self.top_line+self.cursor_y]
        #if line['number']!=None:
        # self.cursor_x = min(self.target_cursor_x, line['width']+1)   

    def scroll_to_cursor(self):
        """ Adjusts the top_line so that the cursor is always visible """
        if self.cursor_y < self.top_line:
            self.top_line = self.cursor_y
        elif self.cursor_y >= self.top_line + self.elements['text'].height:
            self.top_line = self.cursor_y - self.elements['text'].height-1


    def move_cursor(self):
        """ Adjusts the cursor position on the screen """
        #self.logger.warning(f"Cursor {self.name} Move")
            
        screen_y = self.cursor_y + self.elements['text'].top
        screen_x = self.cursor_x + self.elements['text'].left
        
        # dont move if its already there        
        y,x=self.buffer.getyx()
        #if y==screen_y and x==screen_x:
        #    self.logger.warning(f"Cursor Move:Not moving")
        #    return
        info={"y":screen_y,"x":screen_x}
        if y>self.elements['text'].bottom or y<self.elements['text'].top or \
           x>self.elements['text'].right  or x<self.elements['text'].left: 
            self.logger.warning(f"Cursor Move: INVALID LOCATION "+self.dict_log(info))
            return
        try:
            self.buffer.move(screen_y, screen_x)
               
        except Exception as ex:
            self.logger.warning(f"Cursor Move: {ex} "+self.dict_log(info))

    

