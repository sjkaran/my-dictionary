import requests
import sqlite3
from abc import ABC, abstractmethod

class DictionaryDataBase:
    def __init__(self, filename : str = "dictionary.db")-> None:
        self.filename = filename
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()
        print(f"Connected to {self.filename}")


    def create_tables(self):
        self.cursor.execute("""
            CREATE table IF NOT EXISTS dictionary(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            word TEXT UNIQUE NOT NULl,
                            meaning TEXT NOT NULL,
                            type TEXT
                            
                            )
        """)
        self.conn.commit()
        print("table created/verified")

    def search_offline(self, word: str)->str:
        self.cursor.execute("SELECT meaning, type FROM dictionary WHERE word = ?",(word,))
        meaning = self.cursor.fetchone()
        return (meaning[0],meaning[1]) if meaning else None
    
    def upload_data(self,data: tuple)-> bool:
        try:
            self.cursor.execute("INSERT INTO dictionary(word, meaning, type) VALUES (?, ? , ?)",(data[0],data[1],data[2] if len(data)==3 else '' ,))
            self.conn.commit()
        except Exception as e:
            print(f"Error occured: {e}")
            return False
        else:
            print("data pushed successfully.")
            return True


    def searchdict(self,word):
        ...

    def add_or_edit_word(self, word: str, meaning: str,wtype: str = '') -> None:
        try:
            self.cursor.execute("INSERT INTO dictionary(word,meaning,type) VALUES(?,?,?)",(word,meaning,wtype,))
            self.conn.commit()
        except:
            print("failed commiting new word and meaning.")


    def delete_word(self,word: str) -> bool:
        self.cursor.execute("DELETE FROM dictionary WHERE word = ?",(word,))
        self.conn.commit()
    
    def close(self):
        self.cursor.close()


dbm = DictionaryDataBase()

# testing the upload_data function
# upload = dbm.upload_data(('pillow','a soft and bagy thing to use as a support of head while sleeping','noun'))
dbm.upload_data(('terror','something scary or threatning'))
meaning = dbm.search_offline('terror')
if meaning:
    print(meaning)
else:
    print("you did a mistake fuck off.")


dbm.close()

# search offline feature is working.





