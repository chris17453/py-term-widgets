
import curses
from .input import input
from .base import element



class Edit(input):

    def __init__(self, stdscr,filename=None,width=None, height=None,left=0,top=0,read_only=None,show_border=None,show_info=None,show_line_number=None):
        super().__init__(stdscr=stdscr,
                         width=width,
                         height=height,
                         left=left,
                         top=top)
        
        
        self.show_border=show_border
        self.show_info=show_info
        self.show_line_number=show_line_number
        self.filename=filename
        self.target_cursor_x=0
        self.read_only=read_only
        
        self.elements['window']=element(name="Window",left=0,top=0,width=width,height=height)
            
        if self.show_border:
            self.elements['border']=self.elements['window']

            self.padding['left'] +=1
            self.padding['top'] +=1
            self.padding['right'] +=1
            self.padding['bottom'] +=1
        
        if self.show_line_number:
            self.elements['line_numbers']=element(name="line_number",
                                                  left=self.padding['left'],
                                                 top=self.padding['top'],
                                                 width=4,
                                                 bottom=-1, 
                                                 parent=self.elements['window'])
            
            
            self.padding['left'] +=4

        if self.show_info:
            self.elements['info']=element(name="info",
                                          left=self.padding['left'],
                                         top=self.elements['window'].bottom,
                                         bottom=self.elements['window'].bottom,
                                         width=self.elements['window'].width-self.padding['left'],
                                         height=1)


        self.elements['text']=element(name="text",
                                      left=self.padding['left'],
                                        top=self.padding['top'],
                                        width=self.elements['window'].width-self.padding['left']-self.padding['right'],
                                        height=self.elements['window'].height-self.padding['bottom']-self.padding['top'],
                                        parent=self.elements['window'])
        
        for e in self.elements:
            self.logger.info(self.elements[e].info())
        #exit()
        
        if self.filename:
            self.open_file(self.filename)
        
        self.logger.warn(self.padding)
        self.configure()

    def set_active(self):
        self.active=True
        self.update_screen=True
        self.logger.info("Set ACTIVCE")

    def set_inactive(self):
        self.active=None
        self.update_screen=True
        self.logger.info("Set INACTIVCE")

    def run(self):
        """Main loop which renders ui and preforms imput"""
      #  try:
        if self.update_screen==True:
                self.logger.warn("Main Loop")
                self.calcualte_page()
                self.buffer.clear()  
                self.buffer.bkgd(' ', self.colors['BACKGROUND'])

                if self.show_border:
                    self.draw_border()
                if self.show_line_number:
                    self.display_line_numbers()
                if self.show_info:
                    self.display_info()
                self.display_text()
                self.move_cursor()


                # Refresh the buffer
                self.buffer.noutrefresh()
                # Copy the contents of the buffer to the standard screen
                self.update_screen=None

            # get user input , typing, navigation and  command keys
            


      #  except Exception as e:
      #      self.logger.critical(f"Critical error in main: {e}")


