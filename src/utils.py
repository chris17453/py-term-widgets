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
        line=self.lines[self.top_line+self.cursor_y]
        index=line['number']
        self.logger.warning(f"get_text {index}")
        self.logger.warning(line)
        return self.text[index]
    
    def get_line_number(self):
        line=self.lines[self.top_line+self.cursor_y]
        return line['number']

    def get_screen_line(self):
        line=self.lines[self.top_line+self.cursor_y]
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
        if num>=-0:
            line=self.lines[num]
            return line
        return None


    def get_cords(self,line_number,position):
        """Returns the screen cursor position for a given line and character position"""
        for line in self.lines:
            if line['number']==line_number:
                self.logger.warn(line)
                self.logger.warn(position)
                if position >=line['start'] and position <=line['end']:
                    y=line['index']
                    x=position-line['start']
                    self.logger.warning(f"Cords: {x}:{y}")
                    return {'x':x,'y':y}
        return None





