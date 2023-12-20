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
        self.pressed1=None
        self.pressed2=None
        self.released1=None
        self.released2=None
        self.left_click=None
        self.right_click=None
    
    def info(self):
        info=f" \
        Mouse State \n\
        id: {self.id} \n\
        x:  {self.x} \n\
        y:  {self.y} \n\
        z:  {self.z} \n\
        state: {self.state} \n\
        pressed1:     {self.pressed1} \n\
        pressed2:     {self.pressed2} \n\
        released1:    {self.released1} \n\
        released2:    {self.released2} \n\
        left_click:   {self.left_click} \n\
        right_click:  {self.right_click} \n "
        return info

    def update(self):
        self.id, self.x, self.y, self.z, self.state = curses.getmouse()
        if self.state & curses.BUTTON1_PRESSED:
            self.pressed1={'x':self.x,'y':self.y}
            self.released1=None
            self.left_click=None
        if self.state & curses.BUTTON2_PRESSED:
            self.pressed2={'x':self.x,'y':self.y}
            self.released2=None
            self.right_click=None
        if self.state & curses.BUTTON1_RELEASED:
            self.released1={'x':self.x,'y':self.y}
            self.left_click=True
        if self.state & curses.BUTTON2_RELEASED:
            self.released2={'x':self.x,'y':self.y}
            self.right_click=True
        
        

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
        self.ai="ai"
        self.user="user"
        
        
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

        curses.init_pair( 1, curses.COLOR_YELLOW, curses.COLOR_WHITE ) 
        curses.init_pair( 2, 0, 7 )  # INFO
        curses.init_pair( 4, 7, 1)  # BACKGROUND
        curses.init_pair( 5, 14, 8 ) # LINE NUMBERS
        curses.init_pair( 6, 15, 1 )  # Inactive TEXT
        curses.init_pair( 7, 7, 1 )  # Active TEXT
        curses.init_pair( 8, 0, 10 )  # BUTTON
        curses.init_pair( 9, 0, 7 )  # Menu
        curses.init_pair(10, 4, 7 )  # Menu HotKey


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
                self.logger.info("Mouse")
                mouse=True
                instance.update_screen=True
                refresh=True
                key=-1
            if self.active_instance==instance or key==curses.KEY_RESIZE:
                instance.handle_input(key)
            if instance.update_screen==True:
                refresh=True


        for instance in self.instances:
            try:
                if instance.click==True:
                    self.logger.info(f" Window click received: {instance.window.name}")
            except:
                pass

        #if refresh:
        #    self.buffer.clear()

        if refresh or mouse:
            #for y in range(self.window.height,self.window.height,1):
            #    for x in range(self.window.left,self.window.right,1):
            #        self.buffer.
            #self.buffer.bkgd(" ",curses.color_pair(1))
            self.buffer.bkgd(curses.ACS_CKBOARD, curses.color_pair(0))
            self.buffer.erase()
            self.buffer.bkgdset(' ', curses.color_pair(1))
            
            for instance in self.instances:
                if instance is not self.active_instance:
                    instance.run(True)
            
        self.active_instance.run(True)

        if mouse:
            self.handle_mouse()

        self.buffer.noutrefresh()
        curses.doupdate()
        
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
            
        self.mouse.update()
        self.handle_click()

        # record charcter
        #for instance in self.instances:
        #    if mouse_x>instance.window.left
        
        char=self.buffer.instr(self.mouse.y,self.mouse.x, 4)
        attr=self.buffer.inch(self.mouse.y,self.mouse.x)
        
        self.old_char=char.decode('utf-8', errors='ignore')

        # draw mouse
        self.buffer.addstr(self.mouse.y,self.mouse.x,"█")
        self.old_mouse=self.mouse
        
    def handle_click(self):
        self.logger.info(self.mouse.info())
        if self.mouse.pressed1==True:
            self.logger.info("Left Click")
        if self.mouse.pressed2==True:
            self.logger.info("Right Click")

            #for instance in self.instances:
            #    if self.mouse.x>=instance.window.left and  \
            #    self.mouse.x<=instance.window.right and \
            #    self.mouse.y>=instance.window.top and   \
            #    self.mouse.y>=instance.window.bottom:
            #        
            #        self.instance.active()
            
        self.mouse.left_click=None
        self.mouse.right_click=None
                
            

