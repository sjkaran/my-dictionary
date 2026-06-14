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

    def add_data(self, data: tuple) -> bool:
        try:
            if len(data)>=2:
                self.cursor.execute("INSERT INTO dictionary (word, meaning, type) VALUES (?, ? ,?)",(data[0],data[1],data[2] if len(data)==3 else ''))
            else:
                raise ValueError("the word data must contain at least 2 or 3 values")
            return True
        except:
            return False
        
    def edit_data(self,word: str, meaning: str = '', wtype: str = '')-> bool:
        # edit the existing entry in the table.
        try:
            if wtype and meaning:
                self.cursor.execute("UPDATE dictionary SET meaning = ?, type = ? WHERE word = ?",(meaning, wtype, word))
            elif wtype:
                self.cursor.execute("UPDATE dictionary SET type = ? WHERE word = ?",(wtype, word))
            elif meaning:
                self.cursor.execute("UPDATE dictionary SET meaning = ? WHERE word = ?",(meaning, word))
            else:
                raise ValueError("False call, put the value of meaning or word type of a word to update.")
            self.conn.commit()            
            return True
        except Exception as e:
            print("Issue occurred.",e)
            return False

    def delete_word(self,word: str) -> bool:
        self.cursor.execute("DELETE FROM dictionary WHERE word = ?",(word,))
        self.conn.commit()
    
    def see_all_data(self)->None:
        self.cursor.execute("SELECT * FROM dictionary")
        data = self.cursor.fetchall()
        for d in data:
            print(f"{d[0]} . {d[1]} : {d[2]}  . ({d[3] if d[3] else 'Not Defined'})")

    def close(self):
        self.cursor.close()


dbm = DictionaryDataBase()

# testing the upload_data function
# upload = dbm.upload_data(('pillow','a soft and bagy thing to use as a support of head while sleeping','noun'))

#testing the add_or_edit_word()
# dbm.see_all_data()

# dbm.delete_word('terror')   # working fine
# dbm.see_all_data()
# dbm.cursor.execute("SELECT * FROM dictionary WHERE word = ? ",('pillow',))
# print(dbm.cursor.fetchall())

# dbm.edit_data(word = 'pillow',meaning='A Bag like object filled with cushon Helpfull for sleeping.',wtype='Noun')
# dbm.edit_data(word = 'pillow')

dbm.cursor.execute("SELECT * FROM dictionary WHERE word = ? ",('pillow',))
print(dbm.cursor.fetchall())
dbm.close()

# search offline feature is working.





