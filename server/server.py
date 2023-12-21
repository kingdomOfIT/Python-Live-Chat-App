from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

HOST = 'localhost'
PORT = 5501
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
        client = person.client
        if name == "":
            client.send(msg)
        else:
            client.send(bytes(name + ": ", "utf8") + msg)

def client_communication(person):
    """
    Thread to handle all mesages from client
    """
    client = person.client
    
    # first message received is always persones name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "") # broadcast welcome message
    
    while True: # wait for any messages from person
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))
            if msg == bytes("{quit}", "utf8"): # if message is quit disconect client
                client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONECTED] {name} disconected ")
                break
            else: # send message to all clients
                broadcast(msg, name)
        except Exception as e: 
            print(f"[client_communication exception] {e}")
            break

def wait_for_connection(SERVER):
    """
    Wait for connection from new clients, start new thread once connected
    """
    while True:
        try:
            client, addr = SERVER.accept() # wait for any new connections
            person = Person(addr,client) # create new person for connection
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e: 
            print(" wait_for_connection Failure: ", e)
            break
            
    print("Server crashed")

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # open server to listen for connections
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()