import sqlite3
from sqlite3 import Error
from datetime import datetime
import time

# CONSTANT VARIABLES

FILE = "messages.db"
PLAYLIST_TABLE = "Messages"

class DataBase: 
    """ 
    Used to connect, write to and read from a local sqlite3 databse
    """
    def __init__(self):
        """ 
        try to connect to file and create cursor
        """
        self.conn = None
        try: 
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)
            
        self.cursor = self.conn.cursor()
        self._create_table()
        
    def close(self):
        """ 
        Close the db connection
        """
        self.conn.close()
        
    def _create_table(self):
        """ 
        create new databse table if one doesn't exist
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()
    
    def get_all_messages(self, limit=100, name=None):
        """ 
        returns all message
        """
        if not name:
            query = f"SELECT * FROM {PLAYLIST_TABLE}"
            self.cursor.execute(query)
        else: 
            query = f"SELECT * FROM {PLAYLIST_TABLE} WHERE NAME = ?"
            self.cursor.execute(query(name, ))
            
        result = self.cursor.fetchall()
        
        # return messafes in sorted order by date
        results = []
        
        for r in sorted(result, key=lambda x: x[3], reverse = True)[:limit]:
            name, content, date, _id = r
            data = {"name": name, "message": content, "time": str(date)}
            results.append(data)
            
        return list(reversed(results))
    
    def get_messages_by_name(self, name, limit = 100):
        """
        Gets a list of messages by user name
        """
        return self.get_all_messages(limit, name)
    
    def save_message(self, name, msg):
        """
        saves the given message in the table
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.conn.commit()