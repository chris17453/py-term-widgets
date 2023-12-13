
from .io import io
import curses

class ui(io):
    def handle_OOB(self):
        line=self.get_line()
        if line['number']==None:
            for a in range(line['index'],-1,-1):
                if self.lines[a]['number']!=None:
                    break
                self.move_y(distance=-1)
        if self.cursor_x>line['width']:
            self.cursor_x=line['width']

    def move_y(self,distance=None,position=None):
        if position!=None:
            if position<0:
                position=0
            if position>=len(self.lines)-1:
                position=len(self.lines)-1
                self.logger.warning("Scroll Move Y paast end")
            # if its within the curent window view.....
            if position >self.top_line and position <self.top_line+self.height:
                self.logger.warning("Move Y cursor in the window")
                self.cursor_y=position-self.top_line
            else:
                self.logger.warning("Scroll Move Y cursor in the window")
            # otherwise scroll
                self.top_line=position
        elif distance!=None:
            if self.cursor_y+distance>self.height-1:
                self.logger.error("move y bottom")

                # its below the viewport
                if self.top_line+self.height<self.last_screen_line+1:

                    self.logger.error(f"move y bottom top inc {self.top_line} {self.cursor_y}")

                    self.top_line +=1
                    self.cursor_y=self.height-1
            
            elif self.cursor_y+distance<0:
                self.logger.error("move y top")
                # It's above the view port
                self.cursor_y=0
                if self.top_line>0:
                    self.logger.error("move y top dec")
                    self.top_line +=distance
            else:
                # its in the middle of the viewport
                if self.lines[self.top_line+self.cursor_y+distance]['number']!=None:
                    self.logger.error("move y middle")
                    self.cursor_y+=distance
   
    
    def move_x(self,distance=None,position=None):
        if position!=None:
            self.cursor_x = position   
            self.target_cursor_x=self.cursor_x
        elif distance!=None:
            if distance<0:
                if self.cursor_x>=distance:
                    self.cursor_x +=distance
                    if self.cursor_x<0:
                        end=self.get_previous_line()
                        if end['width']==None:
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
                    if self.cursor_x>=self.width-1:
                        self.cursor_x=0
                        self.logger.warn("Calc 1")
                        self.calcualte_page()
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
        self.buffer.border(0)

    def display_text(self):
        wrapped_text = self.wrap_text()
        for idx, line in enumerate(wrapped_text[self.top_line:self.top_line + self.height]):
            self.buffer.addstr(idx + 1, 5, line[:self.width])  # Adjust for line numbers

    def calcualte_page(self):
        try:
            self.lines=[]
            line=0
            screen_line=0
            index=0
            for i in range(max(len(self.text),len(self.text)+self.height)):
                if line<len(self.text):
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
                            text_right=min(text_length,self.width)+text_left
                            if text_left==0:
                                display=line+1
                            else:
                                display=''

                            width=text_right-text_left
                            lines.append({'start':text_left,'end':text_right,'number':line,'width':width,'display':display,'y':i,'line_start':screen_line_start,'mid':0,'index':index})
                            # if this is the line the cursor is on and we are at the end, insert a blank line
                            if index==self.top_line+self.cursor_y and width==self.width and text_length<=self.width:
                                self.temp_line=index

                            if self.temp_line==index:
                                index +=1
                                screen_line +=1
                                lines.append({'start':text_right,'end':text_right,'number':line,'width':0,'display':'','y':i,'line_start':screen_line_start,'CURSOR':0,'index':index})
                                self.logger.warning("Cursor new line")
                            text_left+=self.width
                            text_length -= self.width
                            self.last_screen_line=screen_line
                            screen_line +=1
                            index+=1
                    for a in range(len(lines)):
                        lines[a]['line_end']=screen_line-1
                    line=line+1
                    self.lines+=lines

                else:
                    self.lines.append({'start':None,'end':None,'number':None,'width':0,'display':'','y':i,'line_start':screen_line,'line_end':screen_line,'index':index})
                    index+=1
                    screen_line +=1
            self.save_to_json("debug.json",self.lines)
        except Exception as ex:
            self.logger.Error("Calculate page:"+ex)

    def display_line_numbers(self):
        for i in range(self.height):
            line_num = f"{self.lines[self.top_line+i]['display']} ".ljust(4)
            self.buffer.addstr(i + 1, 1, line_num, curses.color_pair(1))

    def display_info(self):
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
        self.buffer.addstr(self.max_y - 1, 1, info[:self.max_x - 2])
    
    def wrap_text(self):
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
        elif self.cursor_y >= self.top_line + self.height:
            self.top_line = self.cursor_y - self.height+ 3

    def move_cursor(self):
        """ Adjusts the cursor position on the screen """
        screen_y = min(self.cursor_y, self.height) + 1
        screen_x = min(self.cursor_x, self.width)  + 5
        
        info={"y":screen_y,"x":screen_x}
        self.logger.warning("Cursor Move: "+self.dict_log(info))
        
        self.buffer.move(screen_y, screen_x)

    