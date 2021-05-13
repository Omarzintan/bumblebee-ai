import tkinter as tk
from tinydb import TinyDB, Query
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "add_contact"
        self.patterns = ["add new contact", "new contact", "add a new contact"]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

        contact_db_path = self.config['Database']['contacts']
        self.contact_db = TinyDB(contact_db_path)

    def action(self, spoken_text):
        try:
            self.add_contact_details()
            self.bs.respond('Added new contact successfully.')
        except Exception as exception:
            print(exception)
            self.bs.respond('Could not add new contact.')

        return

    '''
    Opens a Tkinter window to allow the user to add a new contact
    to the database.
    Arguments: None
    Return type: <JSON> contact_details_json
    '''

    def add_contact_details(self):
        root = tk.Tk()
        root.geometry("500x150")
        root.title("Add New Contact")
        content = tk.Frame(root)
        content.pack()
        contact_details = {}

        # creating fields
        tk.Label(content, text="Name").grid(
            row=0, column=0, padx=5, sticky='sw')
        tk.Label(content, text="email").grid(
            row=1, column=0, padx=5, sticky='sw')
        tk.Label(content, text="phone").grid(
            row=2, column=0, padx=5, sticky='sw')

        name_entry = tk.Entry(content, width=24)
        email_entry = tk.Entry(content, width=24)
        phone_entry = tk.Entry(content, width=24)
        name_entry.grid(row=0, column=1, padx=5)
        email_entry.grid(row=1, column=1, padx=5)
        phone_entry.grid(row=2, column=1, padx=5)

        # retrieve contact details from window.
        def saveInput():
            Entry = Query()
            contact_details["name"] = str(name_entry.get().lower())
            contact_details["email"] = str(email_entry.get().lower())
            contact_details["phone"] = str(phone_entry.get())
            self.contact_db.upsert(
                contact_details, Entry.name == contact_details["name"]
            )
            root.destroy()

        def clear():
            name_entry.delete(0, "end")
            email_entry.delete(0, "end")
            phone_entry.delete(0, "end")

        # Buttons for saving and clearing
        saveButton = tk.Button(content, text="Save", command=saveInput)
        clearButton = tk.Button(content, text="Clear", command=clear)
        saveButton.grid(row=3, column=1, padx=5, sticky='e')
        clearButton.grid(row=3, column=1, padx=5, sticky='w')

        root.mainloop()

        return contact_details
