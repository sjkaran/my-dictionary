import requests
import json

class Dictionary:
    def __init__(self, filename="dictionary.json"):
        self.filename = filename
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("JSON is not a dictionary")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            with open(self.filename, 'w') as f:
                json.dump({}, f, indent=4)

    def load_file(self):
        with open(self.filename,'r')as file:
            loaded_data = json.load(file)
        return loaded_data

    def show_dictionary(self):
        return self.load_file()
        
    def search_offline(self,word):
        data = self.load_file()
        if word in data:
            return data.get(word)
        else:
            return False

    def upload_data(self,data):
        with open(self.filename, 'w')as file:
            json.dump(data,file,indent=4)

    def searchdict(self,word):
        offline_meaning = self.search_offline(word)

        if offline_meaning:
            return offline_meaning
        
        data = self.load_file()

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
        try:
            response = requests.get(url)
            if response.status_code == 200:
                api_data = response.json()
                meaning = api_data[0]["meanings"][0]["definitions"][0]["definition"]
                data[word]=meaning
                self.upload_data(data)
                return meaning
            else:
                return "Word not found."

        except Exception :
            return "Please check the network connection"

    # --- NEW ADDED FEATURES ---
    
    def add_or_edit_word(self, word, meaning):
        """Feature 2 & 3: Adds a missing word or updates an existing one."""
        data = self.load_file()
        data[word] = meaning
        self.upload_data(data)

    def delete_word(self, word):
        """Feature 4: Deletes a word from the offline storage."""
        data = self.load_file()
        if word in data:
            del data[word]
            self.upload_data(data)
            return True
        return False