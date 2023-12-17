import os
import curses
import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='termy.log')  # Specify the log file name


class EditBASE:
    def __init__(self, stdscr,width=None, height=None,left=0,top=0):
        # Create a logger instance
        self.logger = logging.getLogger('termy')

        self.stdscr = stdscr
        self.text=['']
        self.elements={}
        self.width=0
        self.height=0
        # inner window positing
        self.window_x=5
        self.window_y=1
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
            
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.margin={'left':left,'top':top,'right':0,'bottom':0}
        self.padding={'left':0,'top':0,'right':0,'bottom':0}

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
        
        self.colors={}
        self.colors['BACKGROUND']= curses.color_pair(4)
        self.colors['LINE_NUMBERS']= curses.color_pair(5)
        self.colors['BORDER']= curses.color_pair(4)
        self.colors['INFO']= curses.color_pair(2)
        self.colors['ACTIVE_TEXT']= curses.color_pair(6)
        self.colors['INACTIVE_TEXT']= curses.color_pair(7)

    def configure(self):
        self.width=self.window_width
        self.height=self.window_height
        
        if self.window_width!=None:
            self.max_x=self.window_width
            self.margin['right']=self.max_x-self.window_width
            self.logger.info(f"Setting width explicity {self.window_width}")
        else:
            self.width=self.max_x

        if self.window_height!=None:
            self.max_y=self.window_height
            self.margin['bottom']=self.max_y-self.window_height
            self.logger.info(f"Setting height explicity {self.window_height}")
        else:
            self.height=self.max_y
            
        self.width  -=self.padding['left']+self.padding['right']
        self.height -=self.padding['top']+self.padding['bottom']

        
        # if you dont do the following 2 lines, 
        # the screen will intermittantly glitch
        # on screen resize less than original height
        if self.buffer==None:
            self.buffer = curses.newwin(self.max_y, self.max_x, self.margin['top'], self.margin['left'])
        else:
            self.buffer.resize(self.max_y,self.max_x)
        self.buffer.scrollok(0)
    
        self.update_screen=True





class element:
    def __init__(self,name=None,left=None,top=None,right=None,bottom=None,width=None,height=None,parent=None):

        self.base_left=left
        self.base_top=top
        self.base_width=width
        self.base_height=height
        self.base_bottom=bottom
        self.base_right=right
        self.parent=parent
        self.name=name

        self.left=None
        self.top=None
        self.width=None
        self.height=None
        self.bottom=None
        self.right=None
        
        self.calculate()


    def calculate(self):
        """Recalculates the box's bounding positions based on original settings"""
        
        if self.parent  is not None and \
            self.base_left  is not None and \
            self.base_left<0:
            self.left=self.parent.right+self.base_left
        else: 
            self.left=self.base_left

        if self.parent  is not None and \
            self.base_right  is not None and \
            self.base_right<0:
            self.right=self.parent.right+self.base_right
        else: 
            self.right=self.base_right

        if self.parent is not None and \
            self.base_top is not None and \
            self.base_top<0:
            self.top=self.parent.bottom+self.base_top
        else: 
            self.top=self.base_top

        if self.parent is not None and  \
           self.base_bottom  is not None and  \
           self.base_bottom<0:
           
            self.bottom=self.parent.bottom+self.base_bottom
        else: 
            self.bottom=self.base_bottom

        if self.base_width is not None:
            if self.base_left is None:
                self.left=self.right-(self.base_width)

            if self.base_right is None:
                self.right=self.left+(self.base_width)

        if self.base_height is not None:
            if self.base_top is None:
                self.top=self.bottom-(self.base_height)

            if self.base_bottom is None:
                self.bottom=self.top+(self.base_height)

        if self.left is not None and self.right is not None:
            self.width=self.right-self.left

        if self.top is not None and self.bottom is not None:
            self.height=self.bottom-self.top

        info=self.info()
        if self.left==None:
            raise ValueError(f"Left cannot be none {info}")
        if self.right==None:
            raise ValueError(f"Right cannot be none {info}")
        if self.top==None:
            raise ValueError(f"Top cannot be none {info}")
        if self.bottom==None:
            raise ValueError(f"Bottom cannot be none {info}")
        if  self.width==None:
            raise ValueError(f"Width cannot be none {info}")
        if self.height==None:
            raise ValueError(f"Height cannot be none {info}")



    def info(self):
        info=f"\
                Name: {self.name} \n \
                base_left: {self.base_left}\n \
                base_top: {self.base_top}\n \
                base_width: {self.base_width}\n \
                base_height: {self.base_height}\n \
                base_bottom: {self.base_bottom}\n \
                base_right: {self.base_right}\n \
                parent: {self.parent}\n \
                left: {self.left}\n \
                top: {self.top}\n \
                width: {self.width}\n \
                height: {self.height}\n \
                bottom: {self.bottom}\n \
                right: {self.right}\n"        
        return info

    def set(self,width,height):
        self.base_width=width
        self.height=height
        self.calculate()
    