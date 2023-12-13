import os
import curses
import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='termy.log')  # Specify the log file name


class EditBASE:
    def __init__(self, stdscr,filename=None):
        # Create a logger instance
        self.logger = logging.getLogger('termy')

        self.stdscr = stdscr
        self.filename = filename
        self.text=['']
        #if filename and os.path.exists(filename):
        #    with open(filename, 'r') as file:
        #        self.raw_text = file.readlines()

        self.cursor_x = 0
        self.cursor_y = 0
        self.top_line = 0
        self.last_screen_line=0
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)  # Wait 100ms for input
        self.buffer=None
        self.configure()



    def configure(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.curs_set(2)  # Set cursor to block mode

        #self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.max_y=10
        self.max_x =20
        self.logger.warning(f" X:{self.max_x} , Y:{self.max_y}")
        self.max_y=10 #int(self.max_y/2)
        self.width=self.max_x-6
        self.height=self.max_y-2
        self.target_cursor_x = self.cursor_x
        # if you dont do the following 2 lines, 
        # the screen will intermittantly glitch
        # on screen resize less than original height
        self.stdscr.clear()
        self.stdscr.refresh()    
        if self.buffer==None:
            self.buffer = curses.newwin(self.max_y, self.max_x, 0, 0)
        else:
            self.buffer.resize(self.max_y,self.max_x)
        
        self.update_screen=True
        self.logger.warning("New Buffer Created, update scren set")





            
            
