import customtkinter as ctk
from dictionary import Dictionary
import threading
import sys
import os
import win32com.client
import pythoncom

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

dictionary = Dictionary()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("My Dictionary")
icon_path = resource_path("dicticon.ico")

# --- FIX: Safely load the icon only if it actually exists ---
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Warning: Could not load icon. {e}")
else:
    print(f"Warning: '{icon_path}' not found. Running with default icon.")

# Slightly increased height to elegantly fit the new buttons without ruining the old UI
root.geometry("700x570")

my_x = 700/2

def loading_start():
    loading_bar2.start()
    loading_bar.start()

def loading_stop():
    loading_bar.stop()
    loading_bar2.stop()

def ask_to_add_word(word):
    """Feature 2: Prompts the user to save the word if not found."""
    dialog = ctk.CTkInputDialog(text=f"'{word}' was not found.\nEnter meaning to save it offline:", title="Add Missing Word")
    meaning = dialog.get_input()
    if meaning:
        dictionary.add_or_edit_word(word, meaning)
        output_box.insert("end", f"\n\n[Successfully saved '{word.capitalize()}' to local dictionary!]")

def search_word_thread(word):
    meaning = dictionary.searchdict(word)

    output_box.after(0, lambda: output_box.insert("end",f"{word.capitalize()}:\n{meaning}"))
    output_box.after(0, loading_stop)
    
    # Check if we should trigger Feature 2 (Word not found)
    if meaning == "Word not found.":
        output_box.after(100, lambda: ask_to_add_word(word))



current_searched_word = ""  # The app's short-term memory

def on_search():
    global current_searched_word
    word = entry_box.get().strip().lower()
    output_box.delete("1.0", "end")

    if not word:
        output_box.insert("end", "Please enter a word then search.")
        return
    
    # Save the word to memory before clearing the box
    current_searched_word = word  
    
    loading_start()
    
    entry_box.delete(0, "end") # Box clears, but memory retains the word!

    search_thread = threading.Thread(target=search_word_thread, args=(word,), daemon=True)
    search_thread.start()


def on_clear():
    # entry_box.delete(0,"end")
    output_box.delete("1.0","end")


def on_saved():
    output_box.delete("1.0","end")
    data = dictionary.show_dictionary()

    if not data:
        output_box.insert("end","No Words saved yet.")
        return
    
    for word, meaning in data.items():
        output_box.insert("end",f"{word.capitalize()}:\n")
        output_box.insert("end",f"{meaning}\n \n")


def on_pronounce():
    global current_searched_word
    word = entry_box.get().strip().lower() or current_searched_word
    
    if not word:
        output_box.insert("end", "\n[System: Please search for a word to pronounce.]")
        return
        
    def safe_speak():
        try:
            # 1. Initialize a clean memory state for THIS specific thread
            pythoncom.CoInitialize()
            
            # 2. Directly hook into Windows native text-to-speech (Bypassing pyttsx3)
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(word)
            
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            # 3. CRITICAL: Destroy the object immediately after speaking. 
            # It leaves zero footprint, guaranteeing the next click will work flawlessly.
            pythoncom.CoUninitialize()

    # Spin up a clean, disposable thread every single time you click
    threading.Thread(target=safe_speak, daemon=True).start()



def on_edit():
    global current_searched_word
    word = entry_box.get().strip().lower() or current_searched_word
    
    if not word:
        output_box.insert("end", "\n[System: Please search for a word to edit first.]")
        return
        
    dialog = ctk.CTkInputDialog(text=f"Enter new meaning for '{word}':", title="Edit Word")
    new_meaning = dialog.get_input()
    
    if new_meaning:
        dictionary.add_or_edit_word(word, new_meaning)
        output_box.delete("1.0", "end")
        output_box.insert("end", f"Successfully updated meaning for '{word.capitalize()}'.")



def on_delete():
    global current_searched_word
    word = entry_box.get().strip().lower() or current_searched_word
    
    if not word:
        output_box.insert("end", "\n[System: Please search for a word to delete first.]")
        return
        
    success = dictionary.delete_word(word)
    output_box.delete("1.0", "end")
    
    if success:
        output_box.insert("end", f"Successfully removed '{word.capitalize()}' from saved dictionary.")
        entry_box.delete(0, "end")
        current_searched_word = ""  # Clear memory after deletion
    else:
        output_box.insert("end", f"Could not find '{word.capitalize()}' in saved dictionary.")



#themes
the_blue="#1B287C"
the_skyblue="#23D9E7"

theme=0
def toggle_theme():
    global theme
    if theme==0:
        ctk.set_appearance_mode("light")
        title.configure(font=("Roman",36,"bold"))
        theme+=1
    else:
        ctk.set_appearance_mode("dark")
        theme-=1
    
loading_bar2 = ctk.CTkProgressBar(
    root,
    fg_color=(the_blue,the_skyblue),
    progress_color=(the_skyblue,the_blue),
    orientation="horaizontal",
    width=15,
    corner_radius=1,
    mode="indeterminate",
    determinate_speed=2,
    indeterminate_speed=2
)
loading_bar2.pack(fill="x")


top_bar = ctk.CTkFrame(root, height=50, corner_radius=1,fg_color=("#B6DDE3","#1D2A2C"))
top_bar.pack(fill="x")

title = ctk.CTkLabel(
    top_bar,
    text="DICTIONARY",
    font=("Roman",36),
    text_color=("black","white")
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
    fg_color=(the_blue,the_skyblue),
    progress_color=(the_skyblue,the_blue),
    orientation="horaizontal",
    width=15,
    corner_radius=1,
    mode="determinate",
    determinate_speed=2,
    indeterminate_speed=2
)
loading_bar.pack(fill="x")

card = ctk.CTkFrame(
    root, corner_radius=1
)
card.pack(fill="both",expand=True)

entry_box = ctk.CTkEntry(
    card,
    height=40,
    font=("Arial",18),
    border_color=(the_blue,the_skyblue),
    border_width=1.5,
    fg_color=("white","#58595E"),
    placeholder_text="Enter the word...",
    placeholder_text_color=("black","white"),
    corner_radius=20
)
entry_box.pack(pady=(25,10),padx=50,fill="x")
entry_box.focus()

output_box=ctk.CTkTextbox(
    card,
    height=200,
    corner_radius=20,
    font=("Georgia",16),
    border_color=(the_blue,the_skyblue),
    border_width=1.5,
    wrap="word"
    )
output_box.pack(pady=10,padx=30,fill="both",expand=True)

# ORIGINAL BUTTONS FRAME
btn_frame=ctk.CTkFrame(card,fg_color="transparent")
btn_frame.pack(pady=(10, 5))  # Adjusted padding slightly to fit the new row

search_button = ctk.CTkButton(
    btn_frame,
    text="search",
    font=("Arial",22),
    width=140,
    height=39,
    fg_color=(the_blue,the_skyblue),
    hover_color="blue",
    corner_radius=10,
    command=on_search,
    text_color=("white","black")
)
search_button.pack(side="left",padx=10)

saved_button = ctk.CTkButton(
    btn_frame,
    text="show saved",
    font=("Arial",22),
    width=140,
    height=39,
    fg_color=(the_blue,the_skyblue),
    hover_color="blue",
    corner_radius=15,
    command=on_saved,
    text_color=("white","black")
)
saved_button.pack(side="left",padx=10)

clear_button = ctk.CTkButton(
    btn_frame,
    text="clear",
    font=("Arial",22),
    width=140,
    height=39,
    fg_color=(the_blue,the_skyblue),
    hover_color="blue",
    corner_radius=15,
    command=on_clear,
    text_color=("white","black")
)
clear_button.pack(side="left",padx=10)

# --- NEW FEATURE BUTTONS FRAME ---
action_frame = ctk.CTkFrame(card, fg_color="transparent")
action_frame.pack(pady=(5, 20))

pronounce_button = ctk.CTkButton(
    action_frame,
    text="🔊 Pronounce",
    font=("Arial", 18),
    width=140,
    height=35,
    fg_color=(the_blue,the_skyblue),
    hover_color="blue",
    corner_radius=15,
    command=on_pronounce,
    text_color=("white","black")
)
pronounce_button.pack(side="left", padx=10)

edit_button = ctk.CTkButton(
    action_frame,
    text="✏️ Edit",
    font=("Arial", 18),
    width=140,
    height=35,
    fg_color=(the_blue,the_skyblue),
    hover_color="blue",
    corner_radius=15,
    command=on_edit,
    text_color=("white","black")
)
edit_button.pack(side="left", padx=10)

delete_button = ctk.CTkButton(
    action_frame,
    text="🗑️ Delete",
    font=("Arial", 18),
    width=140,
    height=35,
    fg_color=("#D32F2F", "#F44336"), # A distinct red color for destructive action
    hover_color="#B71C1C",
    corner_radius=15,
    command=on_delete,
    text_color="white"
)
delete_button.pack(side="left", padx=10)


root.bind("<Return>", lambda event: on_search())

root.mainloop()