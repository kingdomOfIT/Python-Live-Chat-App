from flask import Flask, render_template, url_for, redirect, session, request
from flask_socketio import SocketIO
import time
from application import create_app
from application.database import DataBase
import config

# SETUP
app = create_app()
socketio = SocketIO(app) #used for user comunication

# COMUNICATION FUNCTIONS

@socketio.on('event')
def handle_my_custom_event(json, methods= ['GET', 'POST']):
    """ 
    handles saving messages once received from web server
    and sending message to other clients
    """
    data = dict(json)
    if "name" in data:
        db = DataBase()
        db.save_message(data["name"], data["message"])
    
    socketio.emit('message response', json)
    

# MAINLINE
if __name__ == "__main__": #start the web server
    socketio.run(app, debug=True, host=str(config.Config.SERVER))