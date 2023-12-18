
import curses
from .input import input
from .element import element



class Edit(input):

    def __init__(self, 
                 name=None,
                 filename=None,
                 width=None, 
                 height=None,
                 left=0,
                 top=0,
                 right=None,
                 bottom=None,
                 read_only=None,
                 show_border=None,
                 show_info=None,
                 show_line_number=None):
        super().__init__(name=name,
                         width=width,
                         height=height,
                         left=left,
                         top=top,
                         right=right,
                         bottom=bottom)
        
        
        self.show_border=show_border
        self.show_info=show_info
        self.show_line_number=show_line_number
        self.filename=filename
        self.target_cursor_x=0
        self.read_only=read_only
        
        if self.filename:
            self.open_file(self.filename)
        


    def set_active(self):
        self.active=True
        self.update_screen=True
        self.logger.info(f"Set {self.name} ACTIVCE")

    def set_inactive(self):
        self.active=None
        self.update_screen=True
        self.logger.info(f"Set {self.name} INACTIVCE")

    def run(self,update=None):
        """Main loop which renders ui and preforms imput"""
      #  try:
        if self.update_screen==True or update==True:
                #self.logger.warn(f"{self.window.name}: LOOP")

                #id self.margin.top
                self.calcualte_page()
                self.clear_block(self.window.left,
                                 self.window.top,
                                 self.window.width,
                                 self.window.height,
                                 self.colors['BACKGROUND'])

                if self.show_border:
                    self.draw_border()
                if self.show_line_number:
                    self.display_line_numbers()
                if self.show_info:
                    self.display_info()
                self.display_text()
                # only update the cursor if this is the active window
                if self.active==True:
                    #self.logger.warn(f"{self.window.name}: Draw Cursor")

                    self.move_cursor()


                # Refresh the buffer
                # Copy the contents of the buffer to the standard screen
                self.update_screen=None

            # get user input , typing, navigation and  command keys
            


      #  except Exception as e:
      #      self.logger.critical(f"Critical error in main: {e}")

    
    def configure(self):
        super().configure()
        self.padding['left'] =0
        self.padding['top']  =0
        self.padding['right'] =0
        self.padding['bottom'] =0

        self.logger.info(self.window.info())
        if self.show_border:
            self.elements['border']=self.window

            self.padding['left'] +=1
            self.padding['top'] +=1
            self.padding['right'] +=1
            self.padding['bottom'] +=1
        
        if self.show_line_number:
            self.elements['line_numbers']=element(name="line_number",
                                                    left=self.window.left+self.padding['left'],
                                                    top=self.window.top+self.padding['top'],
                                                    width=4,
                                                    bottom=-1, 
                                                    parent=self.window)
            
            
            self.padding['left'] +=4

        if self.show_info:
            self.elements['info']=element(name="info",
                                            left=self.window.left+self.padding['left'],
                                            top=self.window.bottom,
                                            bottom=self.window.bottom,
                                            width=self.window.width-self.padding['left'],
                                            height=1)


        self.elements['text']=element(name="text",
                                        left=self.window.left+self.padding['left'],
                                        top=self.window.top+self.padding['top'],
                                        width=self.window.width-self.padding['left']-self.padding['right'],
                                        height=self.window.height-self.padding['bottom']-self.padding['top'],
                                        parent=self.window)
        
        #for e in self.elements:
        #    self.logger.info(self.elements[e].info())
        #exit()
        #self.logger.info(self.window.info())
        
        
        #self.logger.warn(self.padding)
        
