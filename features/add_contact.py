from tinydb import TinyDB, Query
import PySimpleGUI as sg
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
            self.add_contact_details2()
            self.bs.respond('Added new contact successfully.')
        except Exception as exception:
            print(exception)
            self.bs.respond('Could not add new contact.')

        return

    def add_contact_details(self):
        '''
        Opens a PysimpleGUI window to allow the user to add a new contact
        to the database.
        Arguments: None
        Return type: None
        '''
        sg.theme('DarkAmber')
        layout = [[sg.Text("Name:"), sg.InputText(key="name")],
                  [sg.Text("Email:"), sg.InputText(key="email")],
                  [sg.Text("phone:"), sg.InputText(key="phone")],
                  [sg.Submit(), sg.Cancel()]
                  ]
        event, values = sg.Window("Add Contact", layout).read(close=True)

        Entry = Query()
        contact_details = {}
        contact_details["name"] = str(values['name'].lower())
        contact_details["email"] = str(values['email'].lower())
        contact_details["phone"] = str(values['phone'])
        self.contact_db.upsert(
            contact_details, Entry.name == contact_details["name"]
        )
