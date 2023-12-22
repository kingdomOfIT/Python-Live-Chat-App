from client import Client
import time
from threading import Thread

c1 = Client("Client")
c2 = Client("Person")

def update_messages():
    """ 
    updates the local list of messages
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1) # update every 1/10 of a second
        new_messages = c1.get_messages() # get any new messages from client
        msgs.extend(c1.get_messages()) # add to local list of messages
        
        
        for msg in new_messages: # display new messages 
            # print(msg)
            
            if msg == "{quit}":
                run = False
                break
            
Thread(target=update_messages).start()

c1.send_message("Hello")
time.sleep(4)
c2.send_message("Hello from the other side")
time.sleep(1)
c1.send_message("What's up")
time.sleep(1)
c2.send_message("Same here")
time.sleep(2)

c1.disconect()
time.sleep(2)
c2.disconect()