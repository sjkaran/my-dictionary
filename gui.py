import customtkinter as ctk
from dictionary import Dictionary




# meaning of the word = dictionary.searchdict(word_to_search)

""" showing saved word = data = dictionary.show_dictionary()

    if not data:
        output.insert(tk.END,"No words saved yet.")
        return
    
    for word, meaning in data.items():
        output.insert(tk.END, f"{word}:\n{meaning}\n\n")
"""
        
dictionary = Dictionary()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("My Dictionary")
root.iconbitmap("icon.ico")
root.geometry("700x500")

#themes
the_blue="#1B287C"
the_skyblue="#23D9E7"

theme=0
def toggle_theme():
    global theme
    if theme==0:
        ctk.set_appearance_mode("light")
        theme+=1
    else:
        ctk.set_appearance_mode("dark")
        theme-=1
    
top_bar = ctk.CTkFrame(root, height=50, corner_radius=1,fg_color="#1D2A2C")
top_bar.pack(fill="x")


title = ctk.CTkLabel(
    top_bar,
    text="DICTIONARY",
    font=("Roman",36),
    text_color=("white","white")
)
title.pack(side="left",padx=50,pady=20)


toggle_theme_button = ctk.CTkButton(
    top_bar,
    text="☀️🌘",
    command=toggle_theme,
    border_width=2,
    border_color="#00C1E3",
    fg_color="#1B287C",
    hover_color="#70EFF8",
    text_color="orange",
    width=50,
    height=25,
    font=("Helvetica",9)

)
toggle_theme_button.pack(side="right",padx=20)

loading_bar = ctk.CTkProgressBar(
    root,
    fg_color=(the_skyblue,the_blue),
    progress_color=(the_blue,the_skyblue),
    orientation="horaizontal",
    width=20,
    corner_radius=1
)
loading_bar.pack(fill="x")

card = ctk.CTkFrame(
    root, corner_radius=1
)
card.pack(fill="both",expand=True)

entry_box = ctk.CTkEntry(
    card,
    height=40,
    font=("Georgia",18),
    border_color=(the_blue,the_skyblue),
    border_width=3,
    fg_color=("white","grey"),
    placeholder_text="Enter the word...",
)
entry_box.pack(pady=(25,10),padx=50,fill="x")
entry_box.focus()

output_box=ctk.CTkTextbox(
    card,
    height=200,
    corner_radius=1,
    font=("Georgia",16),
    border_color=(the_blue,the_skyblue),
    border_width=3,
    wrap="word"
    )
output_box.pack(pady=10,padx=30,fill="both",expand=True)


# adding buttons, functions , loading bar movement, next page.



root.mainloop()