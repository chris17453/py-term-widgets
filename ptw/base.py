import os
import curses
import logging

from .element import element

# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='termy.log')  # Specify the log file name


class BASE:
    def __init__(self, 
                 name=None,
                 width=None, 
                 height=None,
                 left=0,
                 top=0,
                 right=None,
                 bottom=None):
        # Create a logger instance
        self.logger = logging.getLogger('termy')
        self.left=left
        self.top=top
        self.right=right
        self.bottom=bottom
        self.buffer = None
        self.text=['']
        self.elements={}
        # inner window positing
        self.name=name
        # element of this window
        self.window=None
        # element parent not base
        self.parent=None
        self.window_width=width
        self.window_height=height
        self.width=self.window_width
        self.height=self.window_height
        self.active=None
        self.read_only=None

        # cursor
        self.cursor_x = 0
        self.cursor_y = 0
        # top line of editor
        self.top_line = 0
        # last line in all of the editor
        self.last_line = 0
        # last line availble for the screen that isnt blank
        self.last_screen_line=0
        
        # screen buffer where all is drawn
        self.buffer=None
            
        
        self.padding={'left':0,'top':0,'right':0,'bottom':0}

           
        self.colors={}
        self.colors['BACKGROUND']= curses.color_pair(4)
        self.colors['LINE_NUMBERS']= curses.color_pair(5)
        self.colors['BORDER']= curses.color_pair(4)
        self.colors['INFO']= curses.color_pair(2)
        self.colors['ACTIVE_TEXT']= curses.color_pair(6)
        self.colors['INACTIVE_TEXT']= curses.color_pair(7)
        self.colors['BUTTON']= curses.color_pair(8)
        self.colors['MENU']= curses.color_pair(9)
        self.colors['MENU_HOTKEY']= curses.color_pair(10)
    
    def info(self):
        info="Class Variables\n"
        for attr in vars(self):
            info+=f"{attr} = {getattr(self, attr)}\n"
        return info



    def close(self):
        #if self.buffer:
        #    self.buffer.endwin()
        pass

    def configure(self):
        self.logger.warning("Re-configuring Window")
        # get the base screens dimentions
        max_y,max_x = self.buffer.getmaxyx()
        
        # set the width of our screen based on preferences or full screen
        #if self.window is None or self.window.parent ==None:
        #w=self.window_width if self.window_width is not None else max_x-self.left
        #h=self.window_height if self.window_height is not None else max_y-self.top
        #if self.right and self.right<0:
        #    w+=self.right
        #if self.bottom and self.bottom<0:
        #    h+=self.bottom
        #else:
        #self.w=w
        #self.h=h
        self.logger.info(self.info())
        # create the main sizing element
        self.window=element(name=f"{self.name} Window",
                            left=self.left,
                            top=self.top,
                            right=self.right,
                            bottom=self.bottom,
                            width=self.width,
                            height=self.height,
                            parent=self.parent)

        # create the buffer for writing to the screen
        # if you dont do the following 2 lines, 
        # the screen will intermittantly glitch
        # on screen resize less than original height

        self.logger.warn(f"{self.window.info()}")
        self.update_screen=True



    def draw_box(self,double_line):
        top=self.window.top
        left=self.window.left
        bottom=self.window.bottom
        height=self.window.height
        width=self.window.width
        c=self.colors['BORDER']
    
        if double_line:
            # Approximation of double line box
            horizontal = '═'  # Unicode U+2550
            vertical = '║'    # Unicode U+2551
            top_left = '╔'    # Unicode U+2554
            top_right = '╗'   # Unicode U+2557
            bottom_left = '╚' # Unicode U+255A
            bottom_right = '╝'# Unicode U+255D
        else:
            # Approximation of single line box
            horizontal = '─'  # Unicode U+2500
            vertical = '│'    # Unicode U+2502
            top_left = '┌'    # Unicode U+250C
            top_right = '┐'   # Unicode U+2510
            bottom_left = '└' # Unicode U+2514
            bottom_right = '┘'# Unicode U+2518

        # Draw top and bottom
        for i in range(left + 1, left + width-1):
            try:
                self.buffer.addstr(top    , i, horizontal, c)
                self.buffer.addstr(bottom , i, horizontal, c)
            except:
                pass

        # Draw sides
        for j in range(top + 1, top + height - 1):
            try:
                self.buffer.addstr(j, left, vertical,c)
                self.buffer.addstr(j, left + width - 1, vertical, c)
            except:
                pass
        try:
            # Draw corners
            self.buffer.addstr(top, left, top_left , c)
            self.buffer.addstr(top, left + width - 1, top_right, c)
            self.buffer.addstr(top + height - 1, left, bottom_left, c)
            self.buffer.addstr(top + height - 1, left + width - 1, bottom_right, c)
        except:
            pass
