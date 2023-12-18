import curses 
import logging
import locale
from .base import element

# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='termy.log')  # Specify the log file name
        


class mouse:
    def __init__(self):
        self.id=0
        self.x=0
        self.y=0
        self.z=0
        self.state=0
    def info(self):
        info=f" \
        id: {self.id} \
        x: {self.x} \
        y: {self.y} \
        z: {self.z} \
        state: {self.state} "
        return info



class Manager():
    def __init__(self,stdscr):
        self.logger = logging.getLogger('termy')
        self.stdscr=stdscr
        self.exit=None
        self.buffer=None
        # Initialize curses

        self.stdscr=curses.initscr()
        # Set locale to support Unicode characters
        locale.setlocale(locale.LC_ALL, '')

        # Clear screen
        curses.use_default_colors()

        if curses.has_colors():
            curses.start_color()
            self.init_colors()

        curses.curs_set(2)  # Set cursor to block mode
        curses.raw()

        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        print("\033[?1003h\n") # allows capturing mouse movement
        curses.flushinp()
        curses.noecho()



        self.stdscr.keypad(True)  # Enable special keys to be captured
        self.stdscr.nodelay(True)
        self.stdscr.timeout(50)  # Wait 100ms for input

        self.instances=[]
        self.active_instance=None
        max_y, max_x = self.stdscr.getmaxyx()
        self.window=element(top=0,left=0,width=max_x,height=max_y)
        self.mouse=mouse()
        self.old_mouse=mouse()
        self.old_char=None
        self.configure()
        
        
    def configure(self):
        max_y, max_x = self.stdscr.getmaxyx()
        self.window.set(width=max_x,height=max_y)
        self.stdscr.clear()
        self.stdscr.refresh()

        if self.buffer==None:
            self.buffer = curses.newwin(self.window.height, self.window.width, self.window.top, self.window.left)
        else:
            self.logger.warning("Resizing")
            self.buffer.resize(self.window.height, self.window.width)

    
    def __del__(self):
        for instance in self.instances:
            instance.close()
        
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        print("\033[?1003l\n"); # Disable mouse movement events, as l = low


    def init_colors(self):
             # Define DOS colors
        dos_colors = [
            (0, 0, 0),           # 0  Black
            (0, 0, 700),        # 1  Blue
            (0, 700, 0),        # 2  Green
            (0, 700, 700),     # 3  Cyan
            (700, 0, 0),        # 4  Red
            (700, 0, 700),     # 5  Magenta
            (700, 700, 0),     # 6  Brown/Yellow
            (750, 750, 750),     # 7  Light Gray
            (500, 500, 500),     # 8  Dark Gray
            (0, 0, 1000),        # 9  Bright Blue
            (0, 1000, 0),        # 10 Bright Green
            (0, 1000, 1000),     # 11 Bright Cyan
            (1000, 0, 0),        # 12 Bright Red
            (1000, 0, 1000),     # 13 Bright Magenta
            (1000, 1000, 0),     # 14 Bright Yellow
            (1000, 1000, 1000)   # 15 Bright White
        ]

        for i, (r, g, b) in enumerate(dos_colors):
            curses.init_color(i, r, g, b)

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE ) 
        curses.init_pair(2, 0, 7 )  # INFO
        curses.init_pair(4, 15, 7)  # BACKGROUND
        curses.init_pair(5, 6, 8 ) # LINE NUMBERS
        curses.init_pair(6, 15, 1 )  # TEXT
        curses.init_pair(7, 15, 9 )  # TEXT
        curses.init_pair(8, 15, 10 )  # BUTTON


    def get_instance(self,direction):
        current_index = self.instances.index(self.active_instance)

        if direction==-1:
            # Get the object before, if it exists
            element = self.instances[current_index - 1] if current_index > 0 else self.instances[-1]
            return element
        elif direction==1:
            # Get the object after, if it exists
            element= self.instances[current_index + 1] if current_index < len(self.instances) - 1 else self.instances[0]
            return element
        
        return None

    def run(self):
        key=self.handle_input()
        
        mouse=None
        refresh=None

        for instance in self.instances:
            if key==curses.KEY_MOUSE:
                mouse=True
                instance.update_screen=True
                refresh=True
                key=-1
            if self.active_instance==instance or key==curses.KEY_RESIZE:
                instance.handle_input(key)
            if instance.update_screen==True:
                refresh=True



        #if refresh:
        #    self.buffer.clear()

        if refresh:
            for instance in self.instances:
    #            if instance is not self.active_instance:
                    instance.run(True)
            
#        self.active_instance.run()

        if mouse:
            self.handle_mouse()

        self.buffer.noutrefresh()
        curses.doupdate()
        
        
    def update_mouse(self):
        self.mouse.id, self.mouse.x, self.mouse.y, self.mouse.z, self.mouse.state = curses.getmouse()


    def add(self,instance,active=None):
        instance.buffer=self.buffer
        if active is not None:
            self.active_instance=instance

        if instance.parent==None:
            instance.parent=self.window
        instance.configure()
        self.instances.append(instance)
    
    def handle_input(self):
        key=self.stdscr.getch()
        if key==curses.KEY_RESIZE:
            self.configure()
        elif key==9: # TAB ->
            if self.active_instance:
                self.active_instance.set_inactive()
            self.active_instance=self.get_instance(1)
            if self.active_instance:
                self.active_instance.set_active()
            #return
        elif key==353: # TAB <-
            if self.active_instance:
                self.active_instance.set_inactive()
            self.active_instance=self.get_instance(-1)
            if self.active_instance:
                self.active_instance.set_active()
            #return
        #elif key==curses.KEY_MOUSE:
        #    self.handle_mouse()
            #key=-1
        elif key == 24:  # Ctrl+X
                self.logger.warning("Input: CTRL X")
                self.exit=True
        return key
    
    def is_wide_char(self,char):
        length=len(char)
        self.logger.warning(f"LEN {length}")
        if length != 1:
            return None
        return True

    def handle_mouse(self):
        #if self.old_char:
        #    if self.is_wide_char(self.old_char) ==True:
        #        self.buffer.instr(self.old_mouse.y,self.old_mouse.x,self.old_char,curses.pair_number(1))
        #        self.logger.warning(f"UNICODE")
#
        #    else:
        #        self.buffer.addstr(self.old_mouse.y,self.old_mouse.x,self.old_char[0],self.old_attr)
        #        self.logger.warning(f"TEXT")
            
        self.update_mouse()

        # record charcter
        #for instance in self.instances:
        #    if mouse_x>instance.window.left
        
        char=self.buffer.instr(self.mouse.y,self.mouse.x, 4)
        attr=self.buffer.inch(self.mouse.y,self.mouse.x)
        
        self.old_char=char.decode('utf-8', errors='ignore')

        # draw mouse
        self.buffer.addstr(self.mouse.y,self.mouse.x,"█")
        self.old_mouse=self.mouse
        
        self.buffer.refresh()
        curses.doupdate()


