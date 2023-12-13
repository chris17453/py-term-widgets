
import curses


from .ui import ui

class input(ui):
    def handle_input(self):
            """Handles user input in the editor."""

            key = self.stdscr.getch()
            self.temp_line=None

            if key == 19:  # Ctrl+S
                self.logger.warning("Input: CRTRL S")
                self.save_file()
            elif key == 24:  # Ctrl+X
                self.logger.warning("Input: CTRL X")
                exit()
                #break  # Exit the editor        
                # 
            
            elif key == curses.KEY_RESIZE:
                self.logger.warning("Input: Window Resize")
            # Resize event
                self.configure()

            #elif key == curses.KEY_PPAGE:
                #self.move_y(distance=-self.height)

            #elif key == curses.KEY_NPAGE:
            #    self.move_y(distance=self.height)

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
            elif key == curses.KEY_DC:
                self.handle_delete()
            elif key == curses.KEY_BACKSPACE :
                self.handle_backspace()
            elif key == 10:  # Enter key
                self.logger.warning("Input: KEY: Enter")
                self.handle_enter()
            elif 0 <= key <= 255:
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
                'width':self.width,
                'height':self.height,
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
            self.logger.warn("Calc Input")

            self.calcualte_page()
            self.move_x(distance=1)
        except Exception as e:
            # Log the error
            self.logger.warning("Parameters: "+self.dict_log(info))
            self.logger.error("Error in handle_character_input: %s", str(e))

    def handle_backspace(self):
        self.logger.warning("Input: KEY: Backspace")

        if self.cursor_x > 0:
            self.logger.warning("backspace 1")
            line=self.get_line()
            self.logger.warning("backspace 2")
            number=self.get_line_number()
            self.logger.warning("backspace 3")
            text = self.get_text()
            self.logger.warning("backspace 4")
            text_len=len(text)
            pos=line['start']+self.cursor_x
            if pos==text_len-1:
                self.logger.warning("backspace gap")
                self.text[number] = text[:pos - 1] 
            else:
                self.logger.warning("backspace mid")
                self.text[number] = text[:pos - 1] + text[pos:]
            self.calcualte_page()
            cords=self.get_cords(number,pos-1)
            if cords!=None:
                self.move_x(position=cords['x'])
                self.move_y(position=cords['y'])
            else:
                self.logger.error("BACKSPACE SNAFU")
        else:
            if self.cursor_y>0:
                number=self.get_line_number()
                text=self.text.pop(number)
                pos=len(self.text[number-1])
                self.text[number-1]+=text
                self.calcualte_page()
                cords=self.get_cords(number-1,pos)
                if cords!=None:
                    self.move_x(position=cords['x'])
                    self.move_y(position=cords['y'])
                else:
                    self.logger.error("BACKSPACE SNAFU")

    def handle_delete(self):
        self.logger.warning("Input: KEY: Delete")
        
        line = self.get_line()
        number=self.get_line_number()
        self.text[number] = line[:self.cursor_x ] + line[self.cursor_x+1:]

                    
    def handle_enter(self):
        try:
            current_line = self.get_line()
            number=current_line['number']
            text=self.text[number]
            self.save_to_json("debug.json",{'lines':self.lines,
                        'line':current_line,
                        'number':number,
                        'width':self.width,'height':self.height,'text':self.text})
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
            self.logger.warn("Calc Enter")

            self.calcualte_page()
            self.move_y(distance=1)
            self.move_x(position=0)
            self.target_cursor_x=self.cursor_x
        except Exception as e:
            # Log the error
            self.logger.error("An error occurred: %s", str(e))
