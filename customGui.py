import customtkinter as ctk
from dictionary import Dictionary
import time


#predefined specific appearence
borderco = "grey"
cornerRa  = 10

# ------------------ Setup ------------------
dictionary = Dictionary()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ------------------ App ------------------
app = ctk.CTk()
app.title("My Dictionary")
app.geometry("600x550")
app.resizable(True, True)

# ------------------ Fade In ------------------
app.attributes("-alpha", 0.0)
def fade_in(alpha=0.0):
    if alpha < 1:
        app.attributes("-alpha", alpha)
        app.after(20, fade_in, alpha + 0.1)
fade_in()

# ------------------ Theme Toggle ------------------
def toggle_theme():
    mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

# ------------------ Top Bar ------------------
top_bar = ctk.CTkFrame(app, height=40, corner_radius=10)
top_bar.pack(fill="x")

title = ctk.CTkLabel(
    top_bar,
    text="My Dictionary",
    font=ctk.CTkFont("Roman",size=30)
)
title.pack(side="left",padx=50)

theme_btn = ctk.CTkButton(
    top_bar,
    text="🌗 Theme",
    width=90,
    fg_color="brown",
    hover_color="black",
    command=toggle_theme
)
theme_btn.pack(side="right", padx=50)

# ------------------ Main Card ------------------
card = ctk.CTkFrame(app, corner_radius=20)
card.pack(fill="both", expand=True, padx=20, pady=20)

# ------------------ Entry ------------------
entry = ctk.CTkEntry(
    card,
    placeholder_text="Enter a word...",
    height=40,
    font=ctk.CTkFont("Georgia",size=14)
)
entry.pack(pady=(25, 10), padx=30, fill="x")
entry.focus()

# ------------------ Output Box ------------------
output = ctk.CTkTextbox(
    card,
    height=260,
    corner_radius=12,
    font=ctk.CTkFont("Georgia",size=13),
    border_color=borderco,
    border_width=1,
    wrap="word"
)
output.pack(pady=10, padx=30, fill="both", expand=True)

# ------------------ Status Bar ------------------
status = ctk.CTkLabel(
    card,
    text="Ready",
    text_color="gray",
    font =ctk.CTkFont( "Georgia", size=12),
    anchor="w"
)
status.pack(fill="x", padx=30, pady=(5, 10))

# ------------------ Logic ------------------
def on_search():
    status.configure(text="Typing")
    # time.sleep(2)
    word = entry.get().strip().lower()
    output.delete("1.0", "end")

    if not word:
        output.insert("end", "⚠️ Please enter a word.")
        return

    status.configure(text="🔍 Searching...")
    app.update_idletasks()

    meaning = dictionary.searchdict(word)

    status.configure(text="Done")
    output.insert("end", f"{word.capitalize()}:\n{meaning}")
    entry.delete(0, "end")

def show_saved():
    output.delete("1.0", "end")
    data = dictionary.show_dictionary()

    if not data:
        output.insert("end", "📭 No words saved yet.")
        return

    for word, meaning in data.items():
        output.insert("end", f"{word.capitalize()}:\n{meaning}\n\n")

def clear_all():
    entry.delete(0, "end")
    output.delete("1.0", "end")
    status.configure(text="🧹 Cleared")

# ------------------ Buttons ------------------
btn_frame = ctk.CTkFrame(card, fg_color="transparent")
btn_frame.pack(pady=10)

search_btn = ctk.CTkButton(
    btn_frame,
    text="Search",
    width=140,
    height=38,
    fg_color="brown",
    hover_color="green",
    corner_radius=10,
    border_color=borderco,
    border_width=1,
    command=on_search
)
search_btn.pack(side="left", padx=6)

saved_btn = ctk.CTkButton(
    btn_frame,
    text="Show Saved",
    width=140,
    height=38,
    corner_radius=cornerRa,
    border_width=1,
    border_color=borderco,
    fg_color="brown",
    command=show_saved
)
saved_btn.pack(side="left", padx=6)

clear_btn = ctk.CTkButton(
    btn_frame,
    text="Clear",
    width=140,
    height=38,
    fg_color="grey",
    hover_color="black",
    command=clear_all
)
clear_btn.pack(side="left", padx=6)

# ------------------ Key Bindings ------------------
app.bind("<Return>", lambda event: on_search())

# ------------------ Run ------------------
if __name__ == "__main__":
    
    app.mainloop()
    
