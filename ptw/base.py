import os
import curses
import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='termy.log')  # Specify the log file name


class EditBASE:
    def __init__(self, stdscr,filename=None,width=None, height=None,x=0,y=0):
        # Create a logger instance
        self.logger = logging.getLogger('termy')

        self.stdscr = stdscr
        self.filename = filename
        self.text=['']

        self.stdscn_x=x
        self.stdscn_y=y
        self.window_x=5
        self.window_y=1
        self.window_width=width
        self.window_height=height
        self.cursor_x = 0
        self.cursor_y = 0
        self.top_line = 0
        self.last_line = 0
        self.last_screen_line=0
        self.buffer=None
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.curs_set(2)  # Set cursor to block mode
        curses.raw()
        self.stdscr.keypad(True)  # Enable special keys to be captured
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)  # Wait 100ms for input
        if self.filename:
           self.open_file(self.filename)
            
        self.configure()



    def configure(self):

        self.max_y, self.max_x = self.stdscr.getmaxyx()
    
        if self.window_width!=None:
            self.max_x=self.window_width
            self.width=self.window_width-6
        else:    
            self.width=self.max_x-6
    
        if self.window_height!=None:
            self.max_y=self.window_height
            self.height=self.window_height-2
        else:    
            self.height=self.max_y-2
        self.logger.warning(f" X:{self.max_x} , Y:{self.max_y}")
    
        self.target_cursor_x = self.cursor_x
        
        # if you dont do the following 2 lines, 
        # the screen will intermittantly glitch
        # on screen resize less than original height
        self.stdscr.clear()
        self.stdscr.refresh()    
        if self.buffer==None:
            self.buffer = curses.newwin(self.max_y, self.max_x, self.stdscn_x, self.stdscn_y)
        else:
            self.buffer.resize(self.max_y,self.max_x)
        
        self.update_screen=True





            
            
