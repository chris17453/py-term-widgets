
import curses
from .input import input



class Edit(input):


    def run(self):
        """Main function to start the text editor."""
        try:
        


            while True:

                if self.update_screen==True:
                    self.logger.error("DRAWING")

            

                    self.buffer.clear()  # Clear the buffer for new drawing
                    self.logger.warn("Calc Main Loop")

                    self.calcualte_page()
                    
                    #self.handle_OOB()
                    
                    self.draw_border()
                    self.display_line_numbers()
                    #self.adjust_cursor()
                    self.display_info()
                    self.display_text()
                    self.move_cursor()

                    # Refresh the buffer
                    self.buffer.noutrefresh()

                    # Copy the contents of the buffer to the standard screen
                    curses.doupdate()
            
                    self.logger.warning("Curses screen update")

                    self.update_screen=None

                    #self.scroll_to_cursor()

                # get user input , typing, navigation and  command keys
                self.handle_input()
                


        except Exception as e:
            self.logger.critical(f"Critical error in main: {e}")


