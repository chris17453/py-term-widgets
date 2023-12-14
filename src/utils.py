import json
from .base import EditBASE

class utils(EditBASE):
    
    def save_to_json(self,filename, array):
        """Saves an array to a JSON file."""
        try:
            with open(filename, 'w') as file:
                json.dump(array, file)
            self.logger.info(f"Array saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")

    def dict_log(self,d):
        """
        Formats a dictionary into a string for logging purposes.

        Args:
        d (dict): The dictionary to format.

        Returns:
        str: A string representation of the dictionary suitable for logging.
        """
        formatted_items = [f"{key}: {value}" for key, value in d.items()]
        return ", ".join(formatted_items)


    def get_line(self):
        return self.lines[self.top_line+self.cursor_y]

    def get_text(self):
        try:
            line=self.lines[self.top_line+self.cursor_y]
            index=line['number']
            self.logger.warning(f"get_text {index}")
            self.logger.warning(line)
            return self.text[index]
        except Exception as ex:
            self.logger.error("get text: {ex}")
    
    def get_line_number(self):
        try:
            line=self.lines[self.top_line+self.cursor_y]
            self.logger.info(f"Line Number {line['number']}")
            return line['number']
        except Exception as ex:
            self.logger.error("get line number: {ex}")

    def get_screen_line(self):
        line=self.lines[self.top_line+self.cursor_y]
        self.logger.info(f"Screen Line Number {line['index']}")
        return line['index']

    def set_text(self,position,text):
        line=self.lines[self.top_line+self.cursor_y]
        index=line['number']
        txt_len=len(self.text[index])
        if position==0:
            # at the start
            self.text[index]=text+self.text[index]
        elif position==txt_len:
            # on the end
            self.text[index]=self.text[index]+text
        elif position>0 and position<txt_len:
            # split it
            self.text[index]=self.text[:position]+text+self.text[position:]
        else:
            self.logger.error("Text input out of bounds")
        return self.text[index]
        
    def get_previous_line(self):
        num=self.top_line+self.cursor_y-1
        if num>=0:
            line=self.lines[num]
            return line
        return None


    def get_cords(self,line_number,position):
        """Returns the screen cursor position for a given line and character position"""
        self.logger.warn(f"In Coords")
        results=[]
        for line in self.lines:
            if line['number']==line_number:
                
                if position >=line['start'] and position <=line['end']:
                    #if line['line_end']!=line['index']:
                    #    continue
                    y=line['index']
                    x=position-line['start']
                    self.logger.warning(f"Cords: {x}:{y}")
                    results.append( {'x':x,'y':y} )
        if len(results) >0 :
                return results[-1]
        self.logger.warn(f"NO Coords found?")
        return None

    def is_end_of_screen_line(self):
        """Returns true if the cursor is at the end of the curent screen line of text"""
        line = self.get_line()
        number=self.get_line_number()
        if self.cursor_x>line['end']:
            return True
        return None

    def is_end_of_line(self):
        """Returns True if cursor is at the end of the screen last screen line for the curent  line of text"""
        line = self.get_line()
        text = self.get_text()
        text_len=len(text)
        if self.cursor_x+line['start']>=text_len:
            return True
        return None
    
    def line_number(self):
        """Returns the curent line number"""
        return self.top_line+self.cursor_y
    
    def text_length(self):
        """Returns the lenth of the text array"""
        return len(self.text)
    
    def line_length(self):
        """Returns the lenth of the curent text line"""
        text=self.get_text()
        text_len=len(text)
        return text_len
    
    
    def update_text(self,text):
        """Updates the curent line of text"""
        try:
            number=self.get_line_number()
            self.text[number]=text
        except Exception as ex:
            self.logger.error(f"Cant update text {ex}")


    def remove_char(self,index):
        """Removes a character from the curent line of text"""
        try:
            text=self.get_text()
            text_len=self.line_length()

            if index>=text_len or index<0:
            # OOB characters
                self.logger.error(f"Cannot remove character from string, OOB {index} of {text_len}")
                return None
            elif text_len==0:
            # zero length strings
                return None
            elif text_len==1 and index==0:
            # single width strings
                text=''

            # multi char strings
            elif index==0:
            # Start of string
                self.logger.error("Removing start")
                text=text[1:]
            elif index==text_len-1:
            # end of string
                self.logger.error(f"Removing end {index} {text_len} '{text}'")
                text=text[:index-1]
            else:
            # charactrers in the middle of text
                self.logger.error("Removing middle")
                text=text[:index] + text[index+1:]
            
            self.update_text(text)
        except Exception as ex:
            self.logger.error("Removing character failed")

    def get_pos(self):
        """returns the character position in a line of text based on the screen cursor"""
        try:
            line=self.get_line()
            pos=line['start']+self.cursor_x
            text_length=self.line_length()
            self.logger.info(f"Curent position is {pos} out of {text_length}")
            if pos>text_length:
                return None
            return pos
        except Exception as ex:
            self.logger.error(f"get position: {ex}")

    

    def find_word_position(self, direction=None):
        try:
            if direction is None:
                return None

            position = self.get_pos()
            if position is None:
                return None
            self.logger.info(f"Position-0001:{position}")

            current_string = self.get_text()
            special_chars='$%#@!`~=_.+-\*()&^[]<>/?,;:\'"{} \t'
            self.logger.info(f"Position-11:{position}")
            if direction == -1:  # Search backwards
                self.logger.info(f"Position-1:{position}")
                if position==0:
                    return position

                position -=1
                # Skip all contiguous white spaces and special characters
                while position >0 and current_string[position] in special_chars:
                    position -= 1

                # Find the nearest non-alphanumeric and non-special character
                while position > 0 and current_string[position - 1].isalnum() and current_string[position - 1] not in special_chars:
                    position -= 1

                return position

            elif direction == 1:  # Search forwards
                if position==len(current_string)-1:
                    return position

                self.logger.info(f"Position0:{position}")
                # Skip all contiguous white spaces and special characters
                self.logger.info(f"Position1:{position}")
                while position < len(current_string) and current_string[position] in special_chars:
                    position += 1
                # Find the next space or end of string after a word
                self.logger.info(f"Position2:{position}")
                while position < len(current_string) and current_string[position].isalnum() and current_string[position] not in special_chars:
                    position += 1

                return position
        except Exception as ex:
            self.logger.error(f"Find word position: {ex}")
        return position

    