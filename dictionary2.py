import requests
import sqlite3
from abc import ABC, abstractmethod
import requests

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

    def search_offline(self, word: str)-> tuple:
        try:
            self.cursor.execute("SELECT meaning,type FROM dictionary WHERE word = ?",(word,))
            meaning = self.cursor.fetchone()
            print(meaning)
            return (meaning[0],meaning[1]) if meaning else None
        except Exception as e:
            print(e)
            return
    
    def upload_data(self,data: tuple)-> bool:
        try:
            self.cursor.execute("INSERT INTO dictionary(word, meaning, type) VALUES (?, ? , ?)",(data[0],data[1],data[2] if len(data)==3 else 'Not Defined.' ,))
            self.conn.commit()
        except Exception as e:
            print(f"Error occured: {e}")
            return False
        else:
            print("data pushed successfully.")
            return True


    def searchdict(self,word):
        offline_meaning = self.search_offline(word)

        if offline_meaning:
            return offline_meaning

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        try:
            response = requests.get(url)
            if response.statuse_code == 200:
                api_data = response.json()
                meaning = api_data[0]["meanings"][0]["definitions"][0]["definition"]
                self.upload_data((word,meaning,))
                return meaning
            else:
                return "Word not found."
            
        except Exception:
            return "Please check the netwrok conncection"

        
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
        try:
            self.cursor.execute("DELETE FROM dictionary WHERE word = ?",(word,))
            self.conn.commit()
            return True
        except:
            return False
    
    def show_dictionary(self)-> list[tuple]:
        self.cursor.execute("SELECT * FROM dictionary")
        data = self.cursor.fetchall()
        return data   # list(tuple(<serial_number>, <word>, <meaning>, <type>),)


    def close(self):
        self.cursor.close()






"""
Changes:
show_dictionary: output: dict -> list[tuple]
search_offline: output: str/bool -> tuple(meanind, type)/bool(False)/None
add_or_edit_word() -> edit_data() : inp3- str (word type), output- bool
delete_word: output: None -> bool.

Untaken:  # json specific
load_file()
upload_data()

New: #sql needed
upload_data() > inserts new data row in the table.
"""

