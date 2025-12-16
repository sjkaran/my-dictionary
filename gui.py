import tkinter as tk
from dictionary import Dictionary

dictionary = Dictionary() # creating an object

root = tk.Tk()
root.title("MY Dictionary App")
root.geometry("500x400")

title = tk.Label(
    root,
    text="Offline Dictionary",
    font=("Arial",18,"bold")
)
title.pack(pady=20)

entry = tk.Entry(root, font=("Arial",14),width=30)
entry.pack(pady=10)

status = tk.Label(
    root,
    text="Ready",
    anchor="w",
    font=("Arial",10),
    relief=tk.SUNKEN
)
status.pack(side=tk.BOTTOM,fill=tk.X)


def on_search():
    word = entry.get().strip().lower()
    output.delete(1.0,tk.END)
    if not word:
        output.insert(tk.END,"Please enter a word.")
        return
    
    status.config(text="Searching...")
    meaning = dictionary.searchdict(word)
    status.config(text="Done")
    output.insert(tk.END,f"{word}:\n{meaning}")
    entry.delete(0,tk.END)

search_btn = tk.Button(
    root,
    text="Search",
    font=("Arial",12),
    command=on_search
)
search_btn.pack(pady=10)


frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

root.bind("<Return>",lambda event: on_search())

output = tk.Text(
    root,
    height=8,
    width=45,
    font=("Arial",12),
    wrap="word",
    yscrollcommand=scrollbar.set
)
output.pack(pady=10)

scrollbar.config(command=output.yview)

def show_saved():
    output.delete(1.0,tk.END)
    data = dictionary.show_dictionary()

    if not data:
        output.insert(tk.END,"No words saved yet.")
        return
    
    for word, meaning in data.items():
        output.insert(tk.END, f"{word}:\n{meaning}\n\n")

show_btn = tk.Button(
    root,
    text="Show Saved Words",
    font=("Arial",11),
    command=show_saved
)
show_btn.pack(pady=5)

def clear_output():
    output.delete(1.0, tk.END)
    entry.delete(0,tk.END)
    status.config(text="Cleared")

clear_btn = tk.Button(
    root,
    text="Clear",
    command=clear_output
)
clear_btn.pack(pady=3)

root.mainloop()