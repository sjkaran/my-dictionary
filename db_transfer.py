import sqlite3
import json

""" Transfering the json data to the sqlite databse manually. (not recommended in the new app)"""
class DB_Transfer:
    def __init__(self, json_filename='dictionary.json', db_filename='dictionary.db'):
        self.json_file = json_filename
        self.db_file = db_filename
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        print(f"Connected to {self.db_file}")

    def load_data(self):
        with open(self.json_file,"r")as jsonfile:
            data = jsonfile.read()
            data = json.loads(data)
        return data

    def data_insert_sql(self,data:tuple)->None:
        self.cursor.execute("INSERT OR IGNORE INTO dictionary (word, meaning, type) VALUES (?, ?, ?)",
                            (data[0], data[1],"None"),)
        self.conn.commit()


run = DB_Transfer()
""" Transfering the json data"""
# datas = run.load_data()
# for data in datas.items():
#     run.data_insert_sql(data)
# print("successfully transfered.")


""" Testing the Transfered data."""
def show_result():
    run.cursor.execute("SELECT * FROM dictionary")
    show = run.cursor.fetchall()
    for i in show:
        print(f"{i[0]}. {i[1]} : {i[2]}")

show_result()





    
