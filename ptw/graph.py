import curses
import random


def init_rgb_color(id, r, g, b):
    # Initialize an RGB color in curses
    curses.init_color(id, int(r * 1000 / 255), int(g * 1000 / 255), int(b * 1000 / 255))


class Graph:
    def __init__(self, stdscr, width, height, start_x, start_y,max_value,right_to_left=None,color="GREY",character=None,top_down=None):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.max_value = max_value
        self.right_to_left = right_to_left
        self.color = color
        self.get_character=character
        self.top_down = top_down


        self.buffer = curses.newwin(height, width, start_y, start_x)
        self.data = [random.uniform(0, 10) for _ in range(width)]
        self.init_colors()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
        curses.curs_set(2)  # Set cursor to block mode
      

    def init_colors(self):
        # Initialize colors and color pairs
        curses.start_color()
        curses.use_default_colors()

        # Define a range of color pairs
        for i in range(1, 16):
            intensity = i * 16 - 1  # Scale intensity from 0 to 255
            color_id = 15 + i  # Custom color ID
            init_rgb_color(color_id, intensity, intensity, intensity)  # Gray scale
            curses.init_pair(i, color_id, -1)  # Pair with default background


    def update_data(self, new_data):
        if self.right_to_left:
            self.data.pop(-1)
            self.data.insert(0, new_data)
        else:
            self.data.pop(0)
            self.data.append(new_data)        


    def get_top_char(self, remainder):
        # Select top character based on the remainder
        if remainder == 0:
            return ' '
        elif remainder == 1:
            return '▁'  # Lower one-eighth block
        elif remainder == 2:
            return '▄'  # Lower quarter block
        elif remainder == 3:
            return '▆'  # Lower three-eighths block

    def get_char_for_height(self, current, max_height):
        # Use different characters based on height
        ratio = current / max_height
        if ratio > 0.75:
            return '█'  # Full block
        elif ratio > 0.5:
            return '▓'  # Dark shade block
        elif ratio > 0.25:
            return '▒'  # Medium shade block
        else:
            return '░'  # Light shade block

    def draw(self):
        self.buffer.clear()
        for i, value in enumerate(self.data):
            scaled_value = int((value / self.max_value) * self.height * 4)  # Multiply by 4 for sub-block precision
            color_pair = int((value / self.max_value) * 10) + 1
            color_pair = min(15, max(1, (scaled_value // (self.height+1 // 15)) + 1))  # Select color pair

            if self.top_down==None:

                for y in range(scaled_value // 4):
                    if self.get_character!=None:
                        char=self.character
                    #else:
                    char = self.get_char_for_height(y, scaled_value)
                    try:
                        self.buffer.addch(self.height - y - 1, i, char, curses.color_pair(color_pair))
                    except Exception as ex:
                        pass
                # Add the top character
                if self.get_character!=None:
                        top_char=self.character
                else:
                    top_char = self.get_top_char(scaled_value % 4)
                try:
                    self.buffer.addch(self.height - (scaled_value // 4) - 1, i, top_char, curses.color_pair(color_pair))
                except Exception as ex:
                    pass
            
            else:
                for x in range(scaled_value // 4):
                    if self.get_character!=None:
                        char=self.character
                    else:
                        char = self.get_char_for_height(x, scaled_value)
                    try:
                        self.buffer.addch(i, x, '█', curses.color_pair(color_pair))
                    except Exception as ex:
                        pass
                # Add the top character
                    if self.get_character!=None:
                                char=self.character
                    else:
                        top_char = self.get_top_char(scaled_value % 4)
                    try:
                        self.buffer.addch(i,(scaled_value // 4) ,  top_char, curses.color_pair(color_pair))
                    except Exception as ex:
                        pass




       # Refresh the buffer
        self.buffer.noutrefresh()
        # Copy the contents of the buffer to the standard screen
        curses.doupdate()



0