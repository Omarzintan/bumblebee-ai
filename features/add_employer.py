from features.default import BaseFeature
import PySimpleGUI as sg
from tinydb import TinyDB, Query


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "add_employer"
        self.patterns = [
            "add new employer",
            "new employer",
            "add a new employer",
            "add a new boss"
        ]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

        employer_db_path = self.config['Database']['employers']
        self.employer_db = TinyDB(employer_db_path)

    def action(self, spoken_text, arguments_list: list = []):
        try:
            self.add_employer_details()
            self.bs.respond('Added new employer successfully.')
        except Exception as exception:
            print(exception)
            self.bs.respond('Could not add new employer.')

        return

    def add_employer_details(self):
        '''
        Opens a PySimpleGui window to allow the user to add a new employer to
        the database.
        Arguments: None
        Return type: None
        '''
        sg.theme('DarkAmber')
        layout = [[sg.Text("Name:"), sg.InputText(key="name")],
                  [sg.Submit(), sg.Cancel()]
                  ]
        event, values = sg.Window("Add Employer", layout).read(close=True)

        Entry = Query()
        employer_details = {}
        employer_details["name"] = str(values['name'].lower())
        self.employer_db.upsert(
            employer_details, Entry.name == employer_details["name"]
        )
