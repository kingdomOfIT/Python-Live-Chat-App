from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

#GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5501
ADDR = (HOST,PORT)
BUFSIZ = 512

#GLOBAL VARIABLES
messages=[]

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def receive_messages():
    """
    receive messages from server
    """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("Testing error: ", e)
            break
        
def send_message(msg):
    """ 
    send messages to server
    """
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()

receive_thread = Thread(target=receive_messages)
receive_thread.start()

send_message("Amir")
time.sleep(3)
send_message("Hello")
time.sleep(3)
send_message("{quit}")