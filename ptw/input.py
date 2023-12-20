
import curses


from .ui import ui

class input(ui):
    def handle_input(self,key):
            """Handles user input in the editor."""


            ## movement commands

            if key == curses.KEY_RESIZE:
                self.logger.warning("Input: Window Resize")
            # Resize event
                self.configure()
            elif key == curses.KEY_PPAGE:
                self.handle_page_up()
            elif key == curses.KEY_NPAGE:
                self.handle_page_down()
            elif key == 542: # CTRL Home
                self.handle_top_document()
            elif key == 537: # CTRL END
                self.handle_end_document()
            elif key == 552: # CTRL RIGHT
                self.handle_skip_left()
            elif key == 567: # CTRL LEFT
                self.handle_skip_right()
            elif key == curses.KEY_HOME:
                self.handle_home()
            elif key == curses.KEY_END:
                self.handle_end()
            elif key == curses.KEY_UP:
                self.handle_up()
            elif key == curses.KEY_DOWN:
                self.handle_down()
            elif key == curses.KEY_LEFT:
                self.handle_left()
            elif key == curses.KEY_RIGHT:
                self.handle_right()
            elif self.read_only:
                return
#            elif key==curses.KEY_MOUSE:
#                self.handle_mouse()
#            key=-1



            ## editable commands

            elif key == 19:  # Ctrl+S
                self.logger.warning("Input: CRTRL S")
                self.save_file()
                # 
            elif key == 27:  # Escape key
                next_ch = self.stdscr.getch()
                if next_ch == ord('s') or next_ch == ord('S'):
                    self.save_file()
            
            elif key == curses.KEY_DC:
                self.handle_delete()
            elif key == curses.KEY_BACKSPACE :
                self.handle_backspace()
            elif key == 10:  # Enter key
                self.logger.warning("Input: KEY: Enter")
                self.handle_enter()
            elif 30 <= key <= 255:
                self.handle_character_input(chr(key))
            elif key==-1:
#                self.logger.warning("Input: KEY:None")
                return
            else:
                self.logger.warning("Input: KEY: UNK Character Input %s",str(key))
                return
            self.update_screen=True

    def handle_home(self):
        self.logger.warning("Input: KEY: Home")
        line_num=self.top_line+self.cursor_y
        screen_y=self.lines[line_num]['line_start']
        screen_x=0

        self.move_y(position=screen_y)
        self.move_x(position=screen_x)

    def handle_end(self):
        self.logger.warning("Input: KEY: End")
        line=self.get_line()

        line_end=line['line_end']
        screen_y=line_end
        screen_x=self.lines[line_end]['width']
        info={'end':line_end,'top':self.top_line,"y":screen_y,"x":screen_x}
        self.logger.warning(self.dict_log(info))
        self.move_y(position=screen_y)
        self.move_x(position=screen_x)       

    def handle_up(self):
        self.logger.warning("Input: KEY: Up")
        self.move_y(distance=-1)
        line=self.get_line()
        if self.target_cursor_x>line['width']:
            self.cursor_x=line['width']
        else:
            self.cursor_x=self.target_cursor_x
            

    def handle_down(self):
        self.logger.warning("Input: KEY: Down")
        self.move_y(distance=1)
        line=self.get_line()
        if self.target_cursor_x>line['width']:
            self.cursor_x=line['width']
        else:
            self.cursor_x=self.target_cursor_x
    
    def handle_left(self):
        self.logger.warning("Input: KEY: Left")
        self.move_x(distance=-1)
        self.target_cursor_x=self.cursor_x
    
    def handle_right(self):
        self.logger.warning("Input: KEY: Right")
        self.move_x(distance=1)
        self.target_cursor_x=self.cursor_x

    def handle_character_input(self, char):
        """Handles character input into the text editor."""

        try:

            line=self.get_line()
            line_num=line['number']
            info={
                'line':line,
                'number':line_num,
                'width':self.elements['text'].width,
                'height':self.elements['text'].height,
                'x':self.cursor_x,
                'y':self.cursor_y,
                'top':self.top_line,
                'text':self.text}
            x_pos=line['start']+self.cursor_x
            text=self.text[line_num] 
            if x_pos==0:
                # start
                self.text[line_num] = char + text
            elif x_pos>=line['end']:
                # end
                self.text[line_num] = text + char 
            else:
                # middle
                self.text[line_num] = text[:x_pos] + char  + text[x_pos:]

            self.calculate_page()
            self.move_x(distance=1)
        except Exception as e:
            # Log the error
            self.logger.error("Error in handle_character_input: %s", str(e))

    def handle_backspace(self):
        self.logger.warning("Input: KEY: Backspace")

        if self.cursor_x > 0:
            # backspacing from the middle or end of line (multi or not)
            line=self.get_line()
            number=self.get_line_number()
            text = self.get_text()
            text_len=len(text)
            pos=line['start']+self.cursor_x
            if pos==text_len-1:
                self.text[number] = text[:pos - 1] 
            else:
                self.text[number] = text[:pos - 1] + text[pos:]
            self.calculate_page()
            cords=self.get_cords(number,pos-1)
            if cords!=None:
                self.move_x(position=cords['x'])
                self.move_y(position=cords['y'])
            else:
                self.logger.error("BACKSPACE SNAFU")
        else:
            if self.cursor_y+self.top_line>0:
                # only pop a line if youre at the beginning of a line (multi or not) and there ia a line above you
                # lines may be split
                line=self.get_line()
                if line['start']==0:
                    # backspacing frm the start of a line
                    number=self.get_line_number()
                    text=self.text.pop(number)
                    pos=len(self.text[number-1])
                    self.text[number-1]+=text
                    self.calculate_page()
                    cords=self.get_cords(number-1,pos)
                    if cords!=None:
                        self.move_x(position=cords['x'])
                        self.move_y(position=cords['y'])
                    else:
                        self.logger.error("BACKSPACE SNAFU")
                else:
                    # backspacing from the start of a multiline that is not the first row 
                    
                    
                    pos=self.get_pos()
                    if pos!=None:
                        self.remove_char(pos-1)
                        number=self.get_line_number()
                        self.calculate_page()
                        cords=self.get_cords(number,pos-2)
                        if cords!=None:
                            self.move_x(position=cords['x'])
                            self.move_y(position=cords['y'])
                        else:
                            self.logger.error("BACKSPACE SNAFU")
                            
                            self.logger.error("BACKSPACE Not in case")
                    else:
                        self.logger.info(f"POS not found")

    def handle_delete(self):
        self.logger.warning("Input: KEY: Delete")
        
        line = self.get_line()
        number=self.get_line_number()
        total_screen_lines=self.screen_lines_length()-1
        screen_line_number=self.line_number()
        
        if self.is_end_of_line()==True:
            if screen_line_number<self.last_screen_line:
                self.logger.warning(f"{line} - {number} {total_screen_lines}")
                # if we are at the end of the line and there is a line below us, pull it up and concat
                text=self.text.pop(number+1)
                self.text[number] +=text
        else:
            # we are in the middle or beginning of a line, and are removing a character
            text=self.get_text()
            pos=line['start']+self.cursor_x
            self.text[number] = text[:pos ] + text[pos+1:]
                    
    def handle_enter(self):
        try:
            current_line = self.get_line()
            number=current_line['number']
            text=self.text[number]
            
            x_pos=current_line['start']+self.cursor_x
            


            if x_pos==0:
                # start so just insert a blank line above
                self.text.insert(number ,'')

            elif x_pos>=current_line['end']:
                # end so just insert a blank line below
                self.text.insert(number+1 ,'')
            else:
                # in the mddle, split it
                self.text[number] = text[:x_pos]
                self.text.insert(number+1 ,text[x_pos:])

            new_line = text[x_pos:]
            # needs a refresh

            self.calculate_page()
            self.move_y(distance=1)
            self.move_x(position=0)
            self.target_cursor_x=self.cursor_x
        except Exception as e:
            # Log the error
            self.logger.error("An error occurred: %s", str(e))

    def handle_skip_left(self):
        """Move the cursor left 1 word to the beginning """
        try:
            cur_pos=self.get_pos()
            if cur_pos==None:
                return None
            pos=self.find_word_position(-1)
            if cur_pos==pos:
            # if it didnt move at all go up 1 line top the end and try again
                number=self.get_line_number()
                if number>0:
                    number -=1
                    line=self.get_previous_line()
                    self.logger.info(line)
                else:
                # already at the top
                    number=0
                    pos=0

            else:
                number=self.get_line_number()
                
            cords=self.get_cords(number,pos)
            
            if cords!=None:
                self.logger.warn(f"CORD SAME: NUM:{number} POS: {pos} Cords:{cords}")
                self.move_x(position=cords['x'])
                self.move_y(position=cords['y'])
        except Exception as ex:
            self.logger.error(f"Skip Left: {ex}")

    def handle_skip_right(self):
        try:
            """Move the cursor right 1 word to the end """
            cur_pos=self.get_pos()
            pos=self.find_word_position(1)

            if cur_pos==pos:
            # if it didnt move at all go up 1 line top the end and try again
                number=self.get_line_number()
                text_len=self.text_length()
                if number<text_len-1:
                    number +=1
                    pos=0
                    cords=self.get_cords(number,pos)
            else:
                number=self.get_line_number()
                cords=self.get_cords(number,pos)
        
            if cords!=None:
                self.move_x(position=cords['x'])
                self.move_y(position=cords['y'])
        except Exception as ex:
            self.logger.error(f"Skip Right: {ex}")

    def handle_top_document(self):
        self.move_x(position=0)
        self.move_y(position=0)

    def handle_end_document(self):
        line=self.lines[self.last_screen_line]
        pos=line['end']
        if pos<0: 
             pos=0

        line_len=self.last_screen_line
        number=line_len-self.elements['text'].height+1
        
        if self.top_line<0:
            self.top_line=0
        self.move_x(position=pos)
        self.top_line=number
        self.move_y(position=self.last_screen_line)

    def handle_page_up(self):
        # pagination = window height... maybe 1 or 2 less for continuity?
        if self.cursor_y>0:
            self.cursor_y=0

        else:
            self.top_line-=self.elements['text'].height
            if self.top_line<0:
                self.top_line=0

    def handle_page_down(self):
        # first page down brings to botrtom of page
        # second brings to next page
        bottom_line=self.elements['text'].height
        for index in range(self.elements['text'].height-1,-1,-1):
            line=self.lines[self.top_line+index]
            if line['end'] is not None:
                bottom_line=index
                break

        
        if self.cursor_y<bottom_line:
            self.cursor_y=bottom_line
        else:
            self.top_line+=self.elements['text'].height
            line_len=self.last_screen_line
            self.logger.warning(f"line len: {line_len} height: {self.elements['text'].height} top:{self.top_line}")
            if self.top_line+self.elements['text'].height>=line_len:
                self.top_line=line_len-self.elements['text'].height+1
            
            if self.top_line<0:
                self.top_line=0

        
    def handle_mouse(self):
        if self.old_char:
            # Extract the character
            char = chr(self.old_char & 0xFF)

            # Extract the attribute (color pair)
            attr = self.old_char & curses.A_COLOR
            self.stdscr.addch(self.old_mouse.y,self.old_mouse.x,char,attr)
            #self.logger.warning(f"--{self.old_char} {char} {attr}")

        
        self.update_mouse()
        
        # record charcter
        #for instance in self.instances:
        #    if mouse_x>instance.window.left
        self.old_char=self.stdscr.inch(self.mouse.y,self.mouse.x)
        ##self.logger.warning(f"--{self.old_char}")
        # draw mouse
        self.stdscr.addch(self.mouse.y,self.mouse.x,"*")
        self.old_mouse=self.mouse
        
        self.stdscr.refresh()





            


