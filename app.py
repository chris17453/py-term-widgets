import curses
import random
import time
import ptw
import os
from chatGPT import ChatGPT


def main(stdscr):
    
    # Initialize multiple graph windows
    graph1=ptw.Graph(stdscr, 50, 14, 0, 10,max_value=10,right_to_left=True)
    #graph2=ptw.Graph(stdscr, 20, 11, 50, 10,max_value=10,right_to_left=None,top_down=True)
    #graph3=ptw.Graph(stdscr, 20, 11, 65, 10,max_value=10,right_to_left=True,top_down=True)
    #graph4=ptw.Graph(stdscr, 50, 11, 80, 10,max_value=10,right_to_left=None,top_down=None)
    
    mgr=ptw.Manager(stdscr)

    history =ptw.Edit(name='history',
                      left=0,
                      top=1 ,
                      
                      height=10,
                      read_only=True,show_border=True,show_line_number=True)
    
    question=ptw.Edit(name='question',
                      height=2,
                      left=00,
                      top=11)
    question.active=True

    copy=ptw.Button(name="Copy",
                           top=13, 
                            left=2,
                            width=10,
                            height=1,
                            text="Copy")

    paste=ptw.Button(name="Paste",
                           top=13, 
                           left=14, 
                            width=10,
                            height=1,
                            text="Paste")

    send=ptw.Button(name="Send",
                           top=13, 
                           right=-2, 
                            width=10,
                            height=1,
                            text="SEND",
                            callback=lambda: send_func(mgr, question, history, ai))

  
    menu=ptw.Menu(name="Menu",
                           top=0, 
                           height=1)
   

    mgr.add(history)
    mgr.add(question,active=True)
    mgr.add(copy)
    mgr.add(paste)
    mgr.add(send)
    mgr.add(menu)
    mgr.add(graph1)
   
    menu.add("File")
    menu.add("Options")
    menu.add("About")

    ai=ChatGPT(os.environ.get('aitui_openai_key')) 
 
    new_data_point=0
    old_data_point=0
    start_time = time.time()

    while True:
        mgr.run()   
        for instance in mgr.instances:
            # NEVER TRIGGERS
            try:
                if instance.click == True:
                    mgr.logger.info("Click Recieved")
            except:
                pass

        current_time = time.time()
        if current_time - start_time >= 0.3:
            start_time = current_time

            lower=min(0,old_data_point+5)
            upper=min(old_data_point+5,25)
            
            old_data_point=new_data_point
            new_data_point=random.randint(lower,upper)
            graph1.update_data(new_data_point)
        if mgr.exit:
            del mgr
            break
        
        #time.sleep(0.1)


def send_func(mgr, question, history, ai):
    mgr.logger.info("Send callback")
    text = question.get_text()
    question.clear()
    history.append(f"{mgr.user} : "+text+"\n")
    resp = ai.send_message(text)
    history.append(f"{mgr.ai} :"+resp+"\n")


if __name__=="__main__":
    curses.wrapper(main)



