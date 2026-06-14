import tkinter as tk
import re
import os
import sys
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
from tkinter import scrolledtext
from tkinter import simpledialog
from setup import generate_key, load_dotenv, encrypt_text, decrypt_text, authenticate

current_file = None

# Menu choice function to call appropriate function
def menu_choice(choice):
    match choice:
        case "Add":
            add_entry()
        case "View":
            list_entries() 
        case "Clear View": 
            clear_view()   
        case "Read":
            read_entry()
        case "Search": 
            search_title() 
        case "Delete":
            delete_item()       
        case "Edit":
            edit_entry() 
        case "Clear":
            clear_entries()
        case "Exit":
            exit() 
                

# Create the default window
root = tk.Tk()
root.title("My Diary App")
root.minsize(width=1000, height=800)
root.config(bg="AntiqueWhite1")

  
# Diary Function
def add_entry():
    # Retrieve content from the single-line Entry widget
    title = title_entry.get()
    content = content_entry.get("1.0", tk.END)
    date = date_entry.get()
    # Encrypt content
    encrypted_content = encrypt_text(content)

    os.makedirs("entries", exist_ok=True)

    file_name = f"{date}_{title}.txt"
    with open(os.path.join("entries", file_name), "wb") as file:
        file.write(encrypted_content)
    result_text_area.config(state=tk.NORMAL)
    result_text_area.delete("1.0", tk.END)    
    result_text_area.insert(tk.INSERT, f"Diary entry '{title}' saved successfully!")
    result_text_area.config(state=tk.DISABLED)

def list_entries():
    entries = os.listdir("entries")
    if entries:
        for index, entry in enumerate(entries, start=1):
            view_text_area.insert(tk.INSERT, f"{index}.{entry}\n")
    else:
        result_text_area.config(state=tk.NORMAL)
        result_text_area.delete("1.0", tk.END)
        result_text_area.insert(tk.INSERT, "No diary entries found.")
        result_text_area.config(state=tk.DISABLED)
        
def clear_view():
    view_text_area.delete("1.0", tk.END)
        
def read_entry():
    file_name = read_name.get().strip()
    file_path = os.path.join("entries", file_name)
    
    try:
        with open(file_path, "rb") as file:
           encrypted_content = file.read()
           content = decrypt_text(encrypted_content)
        
        #Configure text area to be editable, clear it, insert content, disable editing again
        result_text_area.config(state=tk.NORMAL)
        result_text_area.delete("1.0", tk.END)
        result_text_area.insert(tk.INSERT, content)
        result_text_area.config(state=tk.DISABLED)
    except FileNotFoundError:
        result_text_area.config(state=tk.NORMAL)
        result_text_area.delete("1.0", tk.END)
        result_text_area.insert(tk.INSERT, "File not found.")
        result_text_area.config(state=tk.DISABLED)

def search_title():
    entries = os.listdir("entries")
    if entries:
        for index, entry in enumerate(entries, start=1):
            
            result=re.split(r"[_.]", entry)
            keyword=search_entry.get().strip()
            
            if keyword.lower() in result[1].lower():
                file_path = os.path.join("entries", entry)
                try:
                    with open(file_path, "rb") as file:
                       encrypted_content = file.read()
                       content = decrypt_text(encrypted_content)
            
                       #Configure text area to be editable, clear it, insert content, disable editing again
                       result_text_area.config(state=tk.NORMAL)
                       result_text_area.delete("1.0", tk.END)
                       result_text_area.insert(tk.INSERT, content)
                       result_text_area.config(state=tk.DISABLED)
                except FileNotFoundError:
                       result_text_area.config(state=tk.NORMAL) 
                       result_text_area.delete("1.0", tk.END)      
                       result_text_area.insert(tk.INSERT, "File Entry not found.")
                       result_text_area.config(state=tk.DISABLED)
                       
def delete_item():
    entries = os.listdir("entries")
    if entries:
        keyword=delete_entry.get().strip()
        deleted = [entry for entry in entries if keyword.lower() in entry.lower()]
        if deleted:
           for entry in deleted:
               os.remove(os.path.join("entries", entry))
               result_text_area.config(state=tk.NORMAL)
               result_text_area.delete("1.0", tk.END)
               result_text_area.insert(tk.INSERT, f"Deleted: {entry}\n")
               result_text_area.config(state=tk.DISABLED)
        else:
               result_text_area.config(state=tk.NORMAL)
               result_text_area.delete("1.0", tk.END)
               result_text_area.insert(tk.INSERT, "No matching entries.")
               result_text_area.config(state=tk.DISABLED)

def edit_entry():
    global current_file
    
    entries = os.listdir("entries")
    
    if entries:
       #Enter keyword, from title of filename to search 
       keyword = simpledialog.askstring("Search:", "Enter keyword")
       if not keyword: return
       
       for entry in entries:
           if keyword.lower() in entry.lower():
              file_path = os.path.join("entries", entry)
              current_file = file_path
              try:
                  with open(current_file,"rb") as file:
                       encrypted_content = file.read()
                       decrypted_content = decrypt_text(encrypted_content)
                       
                       #Configure text area to be editable, clear it, insert content, disable editing again
                       edit_text_area.config(state=tk.NORMAL)
                       edit_text_area.delete("1.0", tk.END)
                       edit_text_area.insert(tk.INSERT, decrypted_content)
                       
                       edit_text_area.after(30000, save_entry)
              except:
                    result_text_area.insert(tk.INSERT,"Error")
                       
def save_entry():                       
    global current_file
    
    if current_file: 
        file_path = current_file 
        
        try:                 
            modified_content = edit_text_area.get("1.0", tk.END).strip()
            
            result_text_area.config(state=tk.NORMAL)
            result_text_area.delete("1.0", tk.END)
            result_text_area.insert(tk.INSERT, modified_content)
            result_text_area.config(state=tk.DISABLED)
            
            encrypted_modified_content = encrypt_text(modified_content)
            
            with open(file_path, "wb") as file:
                file.write(encrypted_modified_content)
        except Exception as e:
            result_text_area.config(state=tk.NORMAL)
            result_text_area.delete("1.0", tk.END)
            result_text_area.insert(tk.INSERT, f"Error: {str(e)}")
            result_text_area.config(state=tk.DISABLED)
            
def clear_entries():
    date_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    content_entry.delete("1.0", tk.END)
    read_name.delete(0, tk.END)
    search_entry.delete(0,tk.END)
    delete_entry.delete(0, tk.END)
    edit_text_area.delete("1.0", tk.END)
    view_text_area.delete("1.0", tk.END)
    result_text_area.config(state=tk.NORMAL)
    result_text_area.delete("1.0", tk.END)
    result_text_area.config(state=tk.DISABLED)
    
def exit():
    sys.exit()
    
fields = ["Date", "Title", "Content"]

#Create a label frame widget
label_frame=tk.Frame(root,bd=2, width=600, height=50,relief=tk.RIDGE)
label_frame.pack(pady=10, padx=10) 


# Load image
image = Image.open("diary.jpg")
photo = ImageTk.PhotoImage(image)

# Label for title
main_label = tk.Label(label_frame, text="My Diary App", image=photo,compound="left",
                   font=("Times New Roman", 20, "bold"))
main_label.pack(padx=10, pady=10)
     
# 2. OptionMenu Title (Using a Label)
menu_label = tk.Label(root, text="Select your option:", font=("Arial", 10))
menu_label.pack(pady=(10, 3))

# --- NEW: Inline OptionMenu ---
var = tk.StringVar(root)
var.set("Select Settings")
options = ["Add", "View", "Clear View","Read", "Search", "Delete", "Edit", "Clear", "Exit"]

# OptionMenu takes the variable and list, calls function with selection
dropdown = tk.OptionMenu(root, var, *options, command=menu_choice)
dropdown.pack(pady=40)

# 3. Container Frame to hold the three bottom frames together
frame_container = tk.Frame(root)
frame_container.pack(side="top", padx=10, pady=10)

#Prevent root from resizing to fit children's content
frame_container.pack_propagate(False)

# 3. Set the explicit total width and desired 50px height here
frame_container.config(width=950, height=600)

# ---Create a dedicated row frame for the top three items ---
enclosing_frame = tk.Frame(frame_container, bg="lightgray")
# Pack it at the top, spanning across the full width
enclosing_frame.pack(side="top", fill="x", pady=(0, 10)) 

# 4. Left Frame
add_frame = tk.Frame(enclosing_frame, bg="peach puff", borderwidth=3, highlightbackground="AntiqueWhite1", highlightthickness=5,width=300, height=400,relief="ridge")
add_frame.pack_propagate(False)
add_frame.pack(side="left",padx=5, pady=5, anchor="n", expand=True, fill="x")
add_label = tk.Label(add_frame, text="Add Entry").pack(pady=20)

# 5. Middle Frame (Packed next to left)
view_frame = tk.Frame(enclosing_frame, bg="peach puff", borderwidth=3, highlightbackground="AntiqueWhite1", highlightthickness=5,width=300, height=400,relief="ridge")
view_frame.pack_propagate(False)
view_frame.pack(side="left",padx=5, pady=5, anchor="n",expand=True, fill="x")
view_label =tk.Label(view_frame, text="View Entries").pack(pady=20)

# 6. Right Frame (Packed next to middle)
right_frame = tk.Frame(enclosing_frame, bg="peach puff", borderwidth=3, highlightbackground="AntiqueWhite1", highlightthickness=5,width=300, height=400,relief="ridge")
right_frame.pack_propagate(False)
right_frame.pack(side="left",padx=5, pady=5,anchor="n", expand=True, fill="x")
right_label =tk.Label(right_frame, text="Actions").pack(pady=20)

#7. Result Frame (Packed below the three frames)
result_frame = tk.Frame(frame_container, bg="peach puff",borderwidth=3, highlightbackground="AntiqueWhite1", highlightthickness=5, width=600, height=150, relief="ridge")
result_frame.pack_propagate(False)
result_frame.pack(side="bottom", padx=5, pady=5, expand=True, fill="x")
result_label = tk.Label(result_frame, text="RESULT").pack(pady=10)
result_text_area = scrolledtext.ScrolledText(result_frame, width=40, height=10, wrap=tk.WORD)
result_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# --- ROW 1: Date ---
row1 = tk.Frame(add_frame)
row1.pack(fill="x", padx=10, pady=5, side="top") # Stacks first

# Create and pack the Label inside the frame
date_label = tk.Label(row1, text="Date:", width=10, anchor="w")
date_label.pack(side="left")

# Create Entry widget
date_entry = tk.Entry(row1, width=15)
date_entry.pack(side="left",expand=True, fill="x",pady=3)

# --- ROW 2: Title ---
row2 = tk.Frame(add_frame)
row2.pack(fill="x", padx=10, pady=5, side="top")     

# Create and pack the Label inside the frame
title_label = tk.Label(row2, text="Title:", width=10, anchor="w")
title_label.pack(side="left") # side="left" aligns it to the left edge

# Create Entry widget
title_entry = tk.Entry(row2, width=15)
title_entry.pack(side="left",expand=True,fill="x", pady=3)

# --- ROW 3: Content ---
row3 = tk.Frame(add_frame)
row3.pack(fill="x", padx=10, pady=5, side="top")

# Create and pack the Label inside the frame
content_label = tk.Label(row3, text="Content:", width=10, anchor="w")
content_label.pack(side="left", anchor="nw") # side="left" aligns it to the left edge

# Create Entry widget
content_entry = tk.Text(row3, height=15)
content_entry.pack(side="left",expand=True,fill="x",pady=3)

# 1. Create and pack the Label widget
# anchor="w" aligns the text to the left side within its space
view_label = tk.Label(view_frame, text="Content:", font=("Arial", 11))
view_label.pack(side="top", anchor="w", padx=10, pady=(10, 2))

#View Text Area
view_text_area = scrolledtext.ScrolledText(view_frame, width=45, height=10, wrap=tk.WORD)
view_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Insert initial content
view_text_area.insert(tk.INSERT, "Diary Entries:\n")

#Read Label and Entry
read_label = tk.Label(right_frame, text="Read Entry:")
read_label.pack(anchor="w")
read_name = tk.Entry(right_frame, width=15)
read_name.insert(0, "Enter a filename from View.")
read_name.pack(fill=tk.X, pady=(0,15))

#Search Label and Entry
search_label = tk.Label(right_frame, text="Search")
search_label.pack(anchor="w")
search_entry = tk.Entry(right_frame,width=15)
search_entry.insert(0, "Enter keyword from title.")
search_entry.pack(fill=tk.X, pady=(0,15))

#Delete Label and Entry
delete_label = tk.Label(right_frame, text="Delete Entry:")
delete_label.pack(anchor="w")
delete_entry = tk.Entry(right_frame, width=15)
delete_entry.insert(0, "Enter keyword from title.")
delete_entry.pack(fill=tk.X, pady=(0,15))

#Edit Label and Text Area
edit_label = tk.Label(right_frame, text="Edit Entry:")
edit_label.pack(anchor="w")
edit_text_area = scrolledtext.ScrolledText(right_frame, width=40, height=5, wrap=tk.WORD)
edit_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
generate_key()
authenticate()

root.mainloop()
