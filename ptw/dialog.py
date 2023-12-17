#from .base import BASE


#class Dialog(BASE):#
#    def draw():

import curses
import curses

class FloatingDialog:
    def __init__(self, stdscr, width, height, text, title, color_theme=curses.COLOR_WHITE):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.text = text
        self.color_theme = color_theme
        self.buffer = None
        self.title = title

        self.shadow_buffer = None
        self.initialize_colors()
        self.stdscr.clear()
        self.stdscr.refresh()    
        self.configure()

    def initialize_colors(self):
        curses.start_color()
        # Desktop color scheme: white text on blue background
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        # Dialog color scheme: black text on grey background
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        # Close button color scheme: white text on green background
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.stdscr.bkgd(' ', curses.color_pair(1))

    def draw(self):


        # Draw title bar and main dialog
        self.buffer.bkgd(' ', curses.color_pair(2))
        
        self.buffer.box()

        # Draw title
        self.buffer.addstr(0, 1, self.title.center(self.width - 4))

        # Draw close button
        self.buffer.attron(curses.color_pair(3))
        self.buffer.addstr(0, self.width - 3, '[x]', curses.color_pair(3))
        self.buffer.attroff(curses.color_pair(3))

        # Draw text
        for idx, line in enumerate(self.text.split('\n')):
            self.buffer.addstr(idx + 2, 1, line)

        self.buffer.refresh()

    def configure(self):
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.start_x = max(int((self.max_x - self.width) / 2), 0)
        self.start_y = max(int((self.max_y - self.height) / 2), 0)

        if self.width > self.max_x or self.height > self.max_y:
            raise ValueError("Dialog size is larger than the screen.")

        self.buffer = curses.newwin(self.height, self.width, self.start_y, self.start_x)

    def close(self):
        if self.buffer:
            self.buffer.clear()
            self.buffer.refresh()
            self.buffer = None

def main(stdscr):
    curses.curs_set(0)
    dialog = FloatingDialog(stdscr, 40, 12, "Dialog Title", "Hello, world! Press any key to close.")
    dialog.draw()
    stdscr.getch()
    dialog.close()

if __name__ == "__main__":
    curses.wrapper(main)