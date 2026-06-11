import requests
import sqlite3
from abc import ABC, abstractmethod

class Dictionary:
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
        self.cursor.execute("""
        SELECT meaning FROM dictionary word = '?'
        """(word,))
        meaning = self.cursor.fetchall()
        return meaning
    
    def upload_data(self,data):
        ...

    def searchdict(self,word):
        ...

    def add_or_edit_word(self, word: str, meaning: str) -> None:
        ...

    def delete_word(self,word: str) -> bool:
        ...






