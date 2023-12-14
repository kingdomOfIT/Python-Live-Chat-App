from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 1024

#GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name):
    """
    Send new message to all clients 
    """
    for person in persons: 
        client = person.clent
        client.send(bytes(name + ": ", "utf8") + msg)

def client_communication(person):
    """
    Thread to handle all mesages from client
    """
    client = person.client
    #get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    msg = f"{name} has joined the chat!"
    broadcast(msg) #broadcast welcome message
    
    while True:
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))
            if msg == bytes("{quit}", "utf8"):
                broadcast(f"{name} has left the chat...", "Unknown user")
                client.send(bytes("{quit}", "utf8"))
                client.close()
                person.remove(person)
                break
            else: 
                broadcast(msg, name)
        except Exception as e: 
            print(f"[client_communication exception] {e}")
            break

def wait_for_connection(SERVER):
    """
    Wait for connection from new clients, start new thread once connected
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr,client)
            person.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e: 
            print("Failure: ", e)
            run = False
            
    print("Server crashed")

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()