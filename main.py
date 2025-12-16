import requests
import json

class main:
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
        data = self.load_file()
        print(data)

    
    def search_offline(self,word):
        data = self.load_file()
        if word in data:
            print(f"{word} : {data[word]}")
            return True
        else:
            return False

    def upload_data(self,data):
        with open(self.filename, 'w')as file:
            json.dump(data,file,indent=4)

    def searchdict(self,word):
        if self.search_offline(word):
            return
        
        data = self.load_file()

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
        try:
            response = requests.get(url)
            if response.status_code == 200:
                api_data = response.json()

                try:
                    meaning = api_data[0]["meanings"][0]["definitions"][0]["definition"]
                    print(f"{word} : {meaning}")
                    data[word]=meaning
                except (IndexError, KeyError):
                    return f"No simple meaning found for '{word}'."
            else:
                print(f"'{word}' not found.")

            self.upload_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        


    def ui(self):
        while True:
            try:
                word = input("enter the word: ").lower().strip()
                if word=="showDic" or word == "showlist":
                    self.show_dictionary()
                elif word=='q':
                    break
                else:
                    self.searchdict(word=word)
            except Exception as e:
                print("here is the error...",e)
                break
        
        print("\nkeep learning\n")


if __name__=="__main__":
    test = main()
    test.ui()



#feature to add meaning to the words that are not present in the online dictionay.