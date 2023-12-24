import tkinter as tk
from tkinter import messagebox, PhotoImage, Toplevel, Label, Button, Entry, Text, font as tkFont
import json

def save_quests():
    with open("quests.json", "w") as file:
        json.dump(quest_details, file)

def load_quests():
    try:
        with open("quests.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def add_item():
    def submit():
        quest_name = name_entry.get()
        quest_description = desc_entry.get()
        if quest_name:
            listbox.insert(tk.END, quest_name)
            quest_details[quest_name] = quest_description
            new_quest_window.destroy()
            save_quests()

    new_quest_window = Toplevel(root)
    new_quest_window.title("New Quest")

    Label(new_quest_window, text="Quest Name:").pack(padx=10, pady=5)
    name_entry = Entry(new_quest_window)
    name_entry.pack(padx=10, pady=5)

    Label(new_quest_window, text="Description:").pack(padx=10, pady=5)
    desc_entry = Entry(new_quest_window)
    desc_entry.pack(padx=10, pady=5)

    Button(new_quest_window, text="Submit", command=submit).pack(side=tk.LEFT, padx=10, pady=10)
    Button(new_quest_window, text="Cancel", command=new_quest_window.destroy).pack(side=tk.RIGHT, padx=10, pady=10)

    new_quest_window.grab_set()

def delete_item():
    try:
        selected = listbox.curselection()[0]
        del quest_details[listbox.get(selected)]
        listbox.delete(selected)
        hide_description_and_button()
        save_quests()
    except IndexError:
        messagebox.showwarning("Warning", "You must select an item to delete.")

def show_description(event):
    selected = listbox.curselection()
    if selected:
        quest_name = listbox.get(selected[0])
        description_text.config(state=tk.NORMAL)
        description_text.delete('1.0', tk.END)
        description_text.insert(tk.END, quest_details.get(quest_name, ""))
        canvas.itemconfig(description_text_window, state='normal')
        canvas.itemconfig(delete_button_window, state='normal')

def hide_description_and_button():
    canvas.itemconfig(description_text_window, state='hidden')
    canvas.itemconfig(delete_button_window, state='hidden')

# Main window setup
root = tk.Tk()
root.title("Active Quests")
root.geometry("400x600")
root.resizable(False, False)

wood_bg = PhotoImage(file="Wood BG.png")
canvas = tk.Canvas(root, width=400, height=650)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=wood_bg, anchor="nw")

banner_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
bg_image = PhotoImage(file="ScrollV2.png")
banner = tk.Label(root, image=bg_image, text="Active Quests", font=banner_font, compound='center')
banner_window = canvas.create_window(200, 50, window=banner)

add_button = tk.Button(root, text="Start New Quest", command=add_item)
add_button_window = canvas.create_window(200, 160, window=add_button)

delete_button = tk.Button(root, text="Forefit Quest", command=delete_item)
delete_button_window = canvas.create_window(200, 200, window=delete_button)
canvas.itemconfig(delete_button_window, state='hidden')  # Initially hide the delete button

listbox = tk.Listbox(root, width=50)
listbox_window = canvas.create_window(200, 350, window=listbox)
listbox.bind('<<ListboxSelect>>', show_description)

description_text = Text(root, height=4, width=40, state=tk.DISABLED)
description_text_window = canvas.create_window(200, 550, window=description_text)
canvas.itemconfig(description_text_window, state='hidden')  # Initially hide the description box

quest_details = load_quests()

# Populate the listbox with loaded quests
for quest_name in quest_details.keys():
    listbox.insert(tk.END, quest_name)

root.mainloop()
