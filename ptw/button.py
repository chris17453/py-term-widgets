
import curses
from .input import input
from .element import element



class Button(input):

    def __init__(self, 
                 left=None,
                 top=None,
                 name=None,
                 width=None, 
                 height=None,
                 right=None,
                 bottom=None,
                 read_only=None,
                 text=None):
        super().__init__(name=name,
                         width=width,
                         height=height,
                         left=left,
                         top=top,
                         right=right,
                         bottom=bottom)
        
        
        self.read_only=read_only
        self.text=text
        
        


    def set_active(self):
        self.active=True
        self.update_screen=True
        self.logger.info(f"Set {self.name} ACTIVE")

    def set_inactive(self):
        self.active=None
        self.update_screen=True
        self.logger.info(f"Set {self.name} INACTIVE")

    def run(self,update=None):
        """Main loop which renders ui and preforms imput"""
      #  try:
        if self.update_screen==True or update==True:

                #id self.margin.top
                self.clear_block(self.window.left,
                                 self.window.top,
                                 self.window.width,
                                 self.window.height,
                                 self.colors['BUTTON'])

                #self.display_text()
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

        self.elements['text']=element(name="text",
                                        left=self.window.left+self.padding['left'],
                                        top=self.window.top+self.padding['top'],
                                        width=self.window.width-self.padding['left']-self.padding['right'],
                                        height=self.window.height-self.padding['bottom']-self.padding['top'],
                                        parent=self.window)
