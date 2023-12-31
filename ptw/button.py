
import curses
from .base import BASE
from .element import element
from .ui import clear_block


class Button(BASE):

    def __init__(self, 
                 left=None,
                 top=None,
                 name=None,
                 width=None, 
                 height=None,
                 right=None,
                 bottom=None,
                 read_only=None,
                 text=None,
                 callback=None):
        super().__init__(name=name,
                         width=width,
                         height=height,
                         left=left,
                         top=top,
                         right=right,
                         bottom=bottom
                         )
        
        
        self.read_only=read_only
        self.text=text
        self.callback=callback
        self.click=None

        
        


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
        self.click=None
        if self.update_screen==True or update==True:

                #id self.margin.top
                clear_block(self.buffer,self.window.left,
                                 self.window.top,
                                 self.window.width,
                                 self.window.height,
                                 self.colors['BUTTON'])

                #self.display_text()
                # Refresh the buffer
                # Copy the contents of the buffer to the standard screen
                self.buffer.addstr(self.elements['text'].top,
                                    self.elements['text'].left,
                                    self.text,
                                    self.colors['BUTTON'])
                
                self.update_screen=None

            # get user input , typing, navigation and  command keys
            


      #  except Exception as e:
      #      self.logger.critical(f"Critical error in main: {e}")

    
    def configure(self):
        super().configure()
        self.padding['left'] =1
        self.padding['top']  =0
        self.padding['right'] =1
        self.padding['bottom'] =0

        self.elements['text']=element(name="text",
                                        left=self.window.left+self.padding['left'],
                                        top=self.window.top+self.padding['top'],
                                        width=self.window.width-self.padding['left']-self.padding['right'],
                                        height=self.window.height-self.padding['bottom']-self.padding['top'],
                                        parent=self.window)
    def handle_input(self,key):
        if key==curses.KEY_RESIZE:
              self.configure()
        elif key==curses.KEY_ENTER or \
             key==ord(' '):
             self.click=True
             self.logger.info(f" Window click: {self.window.name}")
             if self.callback:
                 self.callback()    

    def get_click(self):
         return self.click
             

         