
import curses
from .input import input



class Edit(input):


    def run(self,stdscr=None):
        """Main loop which renders ui and preforms imput"""
        try:
            if self.update_screen==True:
                self.logger.warn("Main Loop")
                self.calcualte_page()
                self.buffer.clear()  
                self.draw_border()
                self.display_line_numbers()
                self.display_info()
                self.display_text()
                self.move_cursor()

                # Refresh the buffer
                self.buffer.noutrefresh()
                # Copy the contents of the buffer to the standard screen
                curses.doupdate()
        
                self.logger.warning("Curses screen update")
                self.update_screen=None

            # get user input , typing, navigation and  command keys
            self.handle_input()
            


        except Exception as e:
            self.logger.critical(f"Critical error in main: {e}")


