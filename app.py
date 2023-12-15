import curses
import random
import time
import ptw

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    # Initialize multiple graph windows
    graph1=ptw.Graph(stdscr, 50, 11, 0, 10,max_value=10,right_to_left=True)
    graph2=ptw.Graph(stdscr, 20, 11, 50, 10,max_value=10,right_to_left=None,top_down=True)
    graph3=ptw.Graph(stdscr, 20, 11, 65, 10,max_value=10,right_to_left=True,top_down=True)
    graph4=ptw.Graph(stdscr, 50, 11, 80, 10,max_value=10,right_to_left=None,top_down=None)
    
    editor=ptw.Edit(stdscr,height=10,x=0,y=0)

    while True:
        #editor.run()
        
        new_data = random.uniform(0, 10)
        graph1.update_data(new_data)
        graph1.draw()
        graph2.update_data(new_data)
        graph2.draw()
        
        graph3.update_data(new_data)
        graph3.draw()
        graph4.update_data(new_data)
        graph4.draw()
        
        editor.run()
        
        #time.sleep(0.1)



if __name__=="__main__":
    curses.wrapper(main)

