from features.default import BaseFeature
import sys
from tkinter import *
import json
from tinydb import TinyDB, Query


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "add_employer"
        self.patterns = ["add new employer", "new employer", "add a new employer", "add a new boss"]
        super().__init__()
        
        # self.config defined in BaseFeature class
        employer_db_path = self.config['Database']['employers']
        self.employer_db = TinyDB(employer_db_path)



    def action(self, spoken_text):
        try:
            self.add_employer_details()
            self.bs.respond('Added new employer successfully.')
        except:
            print(sys.exc_info())
            self.bs.respond('Could not add new employer.')

        return
    
    '''
    Opens a Tkinter window to allow the user to add a new employer to the database.
    Arguments: None
    Return type: <JSON> employer_details_json
    '''
    def add_employer_details(self):
        root = Tk()
        root.geometry("500x150")
        root.title("Add New Employer")
        content = Frame(root)
        content.pack()
        
        employer_details = {}
        
        # creating fields
        Label(content, text="Name").grid(row=0, column=0, padx=5, sticky='sw')

        name_entry = Entry(content, width=24)
        name_entry.grid(row=0, column=1, padx=5)

        # retrieve employer details from window.
        def saveInput():
            Entry = Query()
            employer_details["name"] = str(name_entry.get().lower())
            self.employer_db.upsert(employer_details, Entry.name == employer_details["name"])
            root.destroy()

        def clear():
            name_entry.delete(0, "end")
        
        # Buttons for saving and clearing
        saveButton = Button(content, text="Save", command=saveInput)
        clearButton = Button(content, text="Clear", command=clear)
        saveButton.grid(row=3, column=1, padx=5, sticky='e')
        clearButton.grid(row=3, column=1, padx=5, sticky='w')

        root.mainloop()

        return employer_details
