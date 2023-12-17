import curses
import random
import time
import ptw

from ptw.base import EditBASE, element

class window_manager():
    def __init__(self,stdscr):
        self.stdscr=stdscr
        # Initialize curses
        #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.use_default_colors()

        if curses.has_colors():
            curses.start_color()

        curses.curs_set(2)  # Set cursor to block mode
        curses.raw()

        stdscr.keypad(True)  # Enable special keys to be captured
        stdscr.nodelay(True)
        stdscr.timeout(50)  # Wait 100ms for input

        self.instances=[]
        self.active_instance=None
        max_y, max_x = self.stdscr.getmaxyx()
        self.window=element(top=0,left=0,width=max_x,height=max_y)
        
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

        key=self.stdscr.getch()
        if key==curses.KEY_RESIZE:
            max_y, max_x = self.stdscr.getmaxyx()
            self.window.set(width=max_x,height=max_y)

            self.stdscr.clear()
            self.stdscr.refresh()
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
        
        for instance in self.instances:
                
            if self.active_instance==instance or key==curses.KEY_RESIZE:
                instance.handle_input(key)
            instance.run()

        self.active_instance.move_cursor()


        curses.doupdate()
        



    def add(self,instance,active=None):
        self.instances.append(instance)
        if active is not None:
            self.active_instance=instance



def main(stdscr):
    
    # Initialize multiple graph windows
    graph1=ptw.Graph(stdscr, 50, 11, 0, 10,max_value=10,right_to_left=True)
    graph2=ptw.Graph(stdscr, 20, 11, 50, 10,max_value=10,right_to_left=None,top_down=True)
    graph3=ptw.Graph(stdscr, 20, 11, 65, 10,max_value=10,right_to_left=True,top_down=True)
    graph4=ptw.Graph(stdscr, 50, 11, 80, 10,max_value=10,right_to_left=None,top_down=None)
    
    mgr=window_manager(stdscr)

    history =ptw.Edit(stdscr,filename="data/parse.c",height=10,left=0,top=0 ,width=mgr.window.width,read_only=True,show_border=True,show_line_number=True)
    
    question=ptw.Edit(stdscr,height=2,left=0,top=10,width=mgr.window.width)
    question.active=True
    mgr.add(history)
    mgr.add(question,active=True)

    while True:


        mgr.run()    
        
        #time.sleep(0.1)



if __name__=="__main__":
    curses.wrapper(main)

