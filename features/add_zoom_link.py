from features.default import BaseFeature
import PySimpleGUI as sg
from tinydb import TinyDB, Query


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "add_zoom_link"
        self.patterns = [
            "add zoom link",
            "new zoom link",
            "add a new zoom class"
        ]
        self.api = bumblebee_api
        self.config = self.api.get_config()
        self.bs = self.api.get_speech()

        zoom_db_path = self.config['Database']['zoom']
        self.zoom_db = TinyDB(zoom_db_path)

    def action(self, spoken_text, arguments_list: list = []):
        try:
            self.add_zoom_details()
            self.bs.respond('Added zoom link successfully.')
        except Exception as exception:
            print(exception)
            self.bs.respond('Could not add zoom link.')

        return

    def add_zoom_details(self):
        '''
        Opens a PySimpleGUI window to allow the user to add a zoom link to the
        database.
        Arguments: None
        Return type: None
        '''
        sg.theme('DarkAmber')
        layout = [[sg.Text("Name:"), sg.InputText(key="name")],
                  [sg.Text("Link:"), sg.InputText(key="link")],
                  [sg.Text("Password (optional):"),
                   sg.InputText(key="password")],
                  [sg.Submit(), sg.Cancel()]
                  ]
        event, values = sg.Window("Add New Zoom link", layout).read(close=True)

        Entry = Query()
        zoom_details = {}
        zoom_details["name"] = str(values['name'].lower())
        zoom_details["link"] = str(values['link'].lower())
        zoom_details["password"] = str(values['password'])
        self.zoom_db.upsert(
            zoom_details, Entry.name == zoom_details["name"]
        )
