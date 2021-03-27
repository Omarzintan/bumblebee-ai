from features.default import BaseFeature
import sys
from tkinter import *
import json
from tinydb import TinyDB, Query


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "add_zoom_link"
        self.patterns = ["add zoom link", "new zoom link", "add a new zoom class"]
        super().__init__()
        
        # self.config defined in BaseFeature class
        zoom_db_path = self.config['Databases']['zoom']
        self.zoom_db = TinyDB(zoom_db_path)



    def action(self, spoken_text):
        try:
            self.add_zoom_details()
            self.bs.respond('Added zoom link successfully.')
        except:
            print(sys.exc_info())
            self.bs.respond('Could not add zoom link.')

        return
    
    '''
    Opens a Tkinter window to allow the user to add a zoom link to the database.
    Arguments: None
    Return type: <JSON> zoom_details_json
    '''
    def add_zoom_details(self):
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
            Entry = Query()
            zoom_details["name"] = str(name_entry.get().lower())
            zoom_details["link"] = str(link_entry.get().lower())
            zoom_details["password"] = str(password_entry.get())
            self.zoom_db.upsert(zoom_details, Entry.name == zoom_details["name"])
            root.destroy()

        def clear():
            name_entry.delete(0, "end")
            link_entry.delete(0, "end")
            password_entry.delete(0, "end")
        
        # Buttons for saving and clearing
        saveButton = Button(content, text="Save", command=saveInput)
        clearButton = Button(content, text="Clear", command=clear)
        saveButton.grid(row=3, column=1, padx=5, sticky='e')
        clearButton.grid(row=3, column=1, padx=5, sticky='w')

        root.mainloop()

        return zoom_details