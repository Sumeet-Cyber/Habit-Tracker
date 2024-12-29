from tkinter import *
import tkinter as tk
import customtkinter as ctk
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# functions-----------

category_button_list = []

# function to create new button for category
def category_buttons(category_list):
    r = 0
    for category in category_list:
        current_cat = category[0]
        button = ctk.CTkButton(categories_frame, text=current_cat)
        button.grid(row=r , column=0, sticky="w")
        r+=1
        category_button_list.append(button)

# function to change category. navigate through categories-----
def change_to_category(index):
    print(f"b number {index + 1} clicked")
    
for i, button in enumerate(category_button_list):
    button.configure(command=lambda index=i: change_to_category(index))
    
 
def fetch_all_categories():
    try:
        with conn:
            cursor.execute("SELECT DISTINCT category FROM tasks")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print("this error occured:", e)

def create_new_table():
    try:
        cursor.execute("""CREATE TABLE tasks (
        category text, 
        name text
        )""")
    except sqlite3.Error as e:
        print(f"error occured: {e}")

def load_tasks(category):
    with conn:
        cursor.execute("SELECT * FROM tasks WHERE category=:category", {'category': category})
        task_list = cursor.fetchall()
        print(task_list)

def delete_existing_category(category):
    pass

# classes======

class Task:
    def __init__(self, category, name):
        self.name = name
        self.category = category
        with conn:
            cursor.execute("INSERT INTO tasks VALUES (:category, :name)", {'category': self.category, 'name': self.name})

    def delete_existing_task(name, category):
        pass
    
    
# -----------------------------------------------------------------------------------------------------------
# Set theme and color
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# main window
root = ctk.CTk()
root.title('Todo application')
WIDTH,HEIGHT = 800, 500
root.geometry(f'{WIDTH}x{HEIGHT}')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1, minsize=100)
root.columnconfigure(1, weight=1, minsize=250)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////
# frames----
# Left side menu frame-
menu_frame_w = WIDTH / 4
menu_frame_h = HEIGHT
menu_frame = ctk.CTkScrollableFrame(master=root, width=menu_frame_w, height=menu_frame_h, fg_color="#2B2B2E", border_width=2, border_color='#ffffff')

menu_frame.rowconfigure(1, weight=1)
menu_frame.columnconfigure(0, weight=1)

menu_frame.grid(row=0, column=0,sticky="nsew")

# Right side task frame-
task_frame_w = WIDTH - menu_frame_w
task_frame_h = HEIGHT
task_frame = ctk.CTkScrollableFrame(master=root, width=task_frame_w, height=task_frame_h, fg_color="#242424", border_width=2, border_color='#ffffff')

task_frame.grid(row=0, column=1, sticky="nsew")

task_frame.rowconfigure(0, weight=1)
task_frame.columnconfigure(0, weight=1)

# /////////////////////////////////////////////////////////////////////////////////////////////////////
# menu window-(window 1)

def button_event():
    print("button pressed")
    create_new_box = ctk.CTkFrame(menu_frame, fg_color='#242424')
    create_new_box.grid_columnconfigure(0, weight=1)
    create_new_box.grid_rowconfigure(0, weight=1)
    create_new_box.grid(row=1, column=0, sticky="ew")

    task_entry = ctk.CTkEntry(create_new_box,
                              placeholder_text="Task Name")
    task_entry.grid(row=0, column=0, sticky="ew")

    def add_task():
        pass
    add_button = ctk.CTkButton(create_new_box, text="Add", command=add_task, width=80)
    add_button.grid(row=1,column=0, sticky="e", pady=10)

button = ctk.CTkButton(menu_frame, text="create new", command=button_event, anchor=CENTER)
button.grid(row=0,column=0, sticky="we", pady=15)



categories_frame = ctk.CTkFrame(menu_frame)
categories_frame.grid(row=2, column=0, sticky="ew")
category_list = fetch_all_categories()
# for i in category_list:
#     print(i[0])
    
category_buttons(category_list)
# print(category_button_list)


# ///////////////////////////////////////////////////////////////////////////////////////////
# task window - (window 2)
# window title---
current_table_name = "some tabledddddddddddd"

title_h = task_frame_h / 10
title_width = task_frame_w
table_title = ctk.CTkLabel(master=task_frame, text = current_table_name, fg_color='#55f0f0', text_color='#ff1100' , compound='top', height=title_h, width=title_width)
table_title.grid(row=0, column=0)


# window tasks--
task_list_h = task_frame_h - title_h
task_list_w = task_frame_w
tasks_list= ctk.CTkLabel(master=task_frame, fg_color='#c0c0c0', height=task_list_h, width=task_list_w)
tasks_list.grid(row=2, column=0)




conn.close()
root.mainloop()