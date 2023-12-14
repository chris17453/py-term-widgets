import curses
import logging
from .edit import Edit



# class inheritance, why.. not sure... 
# base->utils->io->ui->input->edit

def main(stdscr, filename, x, y):
    """Main function to start the text editor."""
    try:
        editor = Edit(stdscr, filename, x, y)
        editor.run()
    except Exception as e:
        editor.logger.critical(f"Critical error in main: {e}")


if __name__ == "__main__":

    filename = "data/parse.c"
    x = 80
    y = 20
    curses.wrapper(lambda stdscr: main(stdscr, filename, x, y))