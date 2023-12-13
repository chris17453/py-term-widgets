import curses
import logging
from .edit import Edit



# class inheritance, why.. not sure... 
# base->utils->io->ui->input->edit

def main(stdscr):
    """Main function to start the text editor."""
    try:
        editor = Edit(stdscr, "example.txt")
        editor.run()
    except Exception as e:
        editor.logger.critical(f"Critical error in main: {e}")


if __name__ == "__main__":
    
    curses.wrapper(main)

