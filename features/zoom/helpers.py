from tkinter import *
import json
from tinydb import TinyDB, Query
import pyperclip as pc
import webbrowser
import os

zoom_db = TinyDB(os.getenv('BUMBLEBEE_PATH')+'features/zoom/zoom_db.json')
'''
Opens a Tkinter window to allow the user to add a zoom link to the database.
Arguments: None
Return type: <JSON> zoom_details_json
'''
def add_zoom_details():
    root = Tk()
    root.geometry("500x150")
    root.title("Add Zoom")
    content = Frame(root)
    content.pack()
    zoom_details = {}

    # creating fields
    Label(content, text="Name").grid(row=0, column=0, padx=5, sticky='sw')
    Label(content, text="Link").grid(row=1, column=0, padx=5, sticky='sw')
    Label(content, text="Password (optional)").grid(row=2, column=0, padx=5, sticky='sw')

    name_entry = Entry(content, width=24)
    link_entry = Entry(content, width=24)
    password_entry = Entry(content, width=24)
    name_entry.grid(row=0, column=1, padx=5)
    link_entry.grid(row=1, column=1, padx=5)
    password_entry.grid(row=2, column=1, padx=5)

    # retrieve zoom details from window.
    def saveInput():
        global zoom_db
        zoom_details["name"] = str(name_entry.get())
        zoom_details["link"] = str(link_entry.get())
        zoom_details["password"] = str(password_entry.get())
        zoom_db.insert(zoom_details)
        print(zoom_db.all())
        root.destroy()

    def clear():
        name_entry.delet(0, "end")
        link_entry.delet(0, "end")
        password_entry.delet(0, "end")
        
    # Buttons for saving and clearing
    saveButton = Button(content, text="Save", command=saveInput)
    clearButton = Button(content, text="Clear", command=clear)
    saveButton.grid(row=3, column=1, padx=5, sticky='e')
    clearButton.grid(row=3, column=1, padx=5, sticky='w')

    root.mainloop()

    return zoom_details

'''Returns all items in zoom_db'''
def show_database():
    for item in zoom_db:
        print(item)

'''Removes all items from zoom_db.'''
def clear_database():
    global zoom_db
    zoom_db.trunctate()

'''Searches for specific item based on its name'''
def search_db(name):
    global zoom_db
    Item = Query()
    print('searching: ', zoom_db)
    results_list = zoom_db.search(Item.name == name)
    return results_list

'''
Opens zoom link based on given name.
Arguments: <string> name
Return type: <boolean> found, <boolean> has_password
'''
def open_zoom(name):
    has_password = False
    found = False
    search_results = search_db(name)
    print('search:', search_results)
    if not search_results:
        return found, has_password
    found = True
    # current policy is to use the first search result from search_db
    result = search_results[0]
    if result['password']:
        has_password = True
        # copy password to clipboard
        pc.copy(result.password)
    webbrowser.open(result['link'])
    return found, has_password

'''
Parse spoken text to retrieve a search query for Zoom.
Arguments: <string> spoken_text, <list> keywords
Return type: <string> spoken_text (now stripped down to only the search query.)
'''
def get_search_query(spoken_text, keywords):
    for word in keywords:
        spoken_text = spoken_text.replace(word, '')
         # Need to remove all whitespace, otherwise the zoom_db search will return nothing.
        spoken_text = spoken_text.replace(' ', '')
    return spoken_text
