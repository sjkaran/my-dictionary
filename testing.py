import requests

def get_meaning(word):
    # API URL
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    # Make the HTTP GET request
    response = requests.get(url)

    # If successful response
    if response.status_code == 200:
        data = response.json()
        
        # Navigate into the first definition
        try:
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return f"Meaning of '{word}': {meaning}"
        except (IndexError, KeyError):
            return f"No simple meaning found for '{word}'."
    else:
        return f"Word '{word}' not found."

# Example
print(get_meaning("hello"))
