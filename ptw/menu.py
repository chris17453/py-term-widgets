
import curses
from .base import BASE
from .element import element
from .ui import clear_block


class Menu(BASE):

    def __init__(self, 
                 left=None,
                 top=None,
                 name=None,
                 width=None, 
                 height=None,
                 right=None,
                 callback=None):
        super().__init__(name=name,
                         width=width,
                         height=height,
                         left=left,
                         top=top,
                         right=right,
                         bottom=top
                         )
        
        
        self.callback=callback
        self.click=None
        self.menu=[]

        
        


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
                                 self.colors['MENU'])

                for key in self.elements:
                    element=self.elements[key]
                    self.buffer.addstr(element.top,
                                        element.left,
                                        element.name[0],
                                        self.colors['MENU_HOTKEY'])

                    self.buffer.addstr(element.top,
                                        element.left+1,
                                        element.name[1:],
                                        self.colors['MENU'])

                    
                
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

  
    def handle_input(self,key):
        if key==curses.KEY_RESIZE:
              self.configure()
        elif key==curses.KEY_ENTER or \
             key==ord(' '):
             self.click=True
             self.logger.info(f" Window click: {self.window.name}")
             if self.callback:
                 self.callback()    

    def add(self,menu):
        menu_len=0
        for item in self.menu:
              menu_len+=len(item)+2
              self.logger.info(f"{item}:{menu_len}")
         
        self.menu.append(menu)
              
        self.elements[menu]=element(name=menu,
                                    left=self.window.left+menu_len+3,
                                    top=self.window.top,
                                    width=len(menu),
                                    height=1,
                                    parent=self.window)



         