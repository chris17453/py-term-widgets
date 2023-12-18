import curses
import random
import time
import ptw




def main(stdscr):
    
    # Initialize multiple graph windows
    graph1=ptw.Graph(stdscr, 50, 11, 0, 10,max_value=10,right_to_left=True)
    graph2=ptw.Graph(stdscr, 20, 11, 50, 10,max_value=10,right_to_left=None,top_down=True)
    graph3=ptw.Graph(stdscr, 20, 11, 65, 10,max_value=10,right_to_left=True,top_down=True)
    graph4=ptw.Graph(stdscr, 50, 11, 80, 10,max_value=10,right_to_left=None,top_down=None)
    
    mgr=ptw.Manager(stdscr)

    history =ptw.Edit(name='history',
                      filename="data/parse.c",
                      left=10,
                      top=1 ,
                      right=-10,
                      height=10,
                      read_only=True,show_border=True,show_line_number=True)
    
    question=ptw.Edit(name='question',
                      height=2,
                      left=10,
                      right=-20,
                      top=11)
    question.active=True
    send_button=ptw.Button(name="Send",
                           top=10, 
                           right=-2, 
                            width=10,
                            height=1,
                            text="SEND")
    mgr.add(history)
    mgr.add(question,active=True)
    mgr.add(send_button)

    while True:

        mgr.run()    
        if mgr.exit:
            del mgr
            break
        
        #time.sleep(0.1)


if __name__=="__main__":
    curses.wrapper(main)

