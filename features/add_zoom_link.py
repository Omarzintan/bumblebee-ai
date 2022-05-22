from features.default import BaseFeature
import PySimpleGUI as sg
import pytermgui as ptg
from tinydb import TinyDB, Query
import tempfile
import subprocess
import json


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
            self.term_enter_zoom_details()
            self.bs.respond('Added zoom link successfully.')
        except Exception as exception:
            print(exception)
            self.bs.respond('Could not add zoom link.')
        return

    def add_zoom_details(self):
        '''
        DEPRECATED.
        Opens a PySimpleGUI window to allow the user to add a zoom link to the
        database.
        Arguments: None
        Return type: None
        This will be deprecated soon
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

    def enter_zoom_details(self):
        '''
        DEPRECATED.
        Allows user to enter zoom details in a GUI window.
        '''
        with ptg.WindowManager() as manager:
            name_field = ptg.InputField(prompt="Name:", expect=str)
            link_field = ptg.InputField(prompt="Link:", expect=str)
            window = ptg.Window(
                ptg.Label("[210 bold]Hello world!"),
                ptg.Label(),
                name_field,
                link_field,
                ptg.Label(),
                ptg.Button("Submit!", lambda *_: manager.stop())
            )
            manager.add(window)
            manager.run()
            print(name_field.get_lines())
            print(link_field.get_lines())

    def term_enter_zoom_details(self):
        '''
        Allows user to enter zoom details within the terminal
        '''
        name = self.bs.ask_question("What is the name for this zoom link?")
        link = input("Please paste the zoom link here")
        password = input("Please enter the password for the zoom link. Press enter if \
            there is no password.")
        if self.bs.approve("Would you like to edit your entry?"):
            edited_zoom_details = self.term_edit_zoom_details(
                name, link, password)
            edited_zoom__details_json = json.loads(edited_zoom_details)
            name = edited_zoom__details_json["name"]
            link = edited_zoom__details_json["link"]
            password = edited_zoom__details_json["password"]
        Entry = Query()
        zoom_details = {}
        zoom_details["name"] = name.lower()
        zoom_details["link"] = link.lower()
        zoom_details["password"] = password
        self.zoom_db.upsert(
            zoom_details, Entry.name == zoom_details["name"]
        )

    def term_edit_zoom_details(self, name, link, password):
        '''
        This allows the user to edit their entry using the nano
        editor.
        '''
        f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        n = f.name
        f.writelines([name, '\n', link, '\n', password])
        f.close()
        subprocess.call(['nano', n])
        with open(n, 'r') as f:
            name = f.readline()
            link = f.readline()
            password = f.readline()
        zoom_details = {}
        zoom_details["name"] = name.lower()
        zoom_details["link"] = link.lower()
        zoom_details["password"] = password
        zoom_details_json = json.dumps(zoom_details)
        return zoom_details_json
