'''Loads routine files into the routine database.'''
from features.default import BaseFeature
from tinydb import TinyDB, Query
import os


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "load_routines"
        self.patterns = [
            "load routines", "update routines database"
        ]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()
        self.routines_folder_path = self.config["Folders"]["routines"]

        routines_db_path = self.config['Database']['routines']
        self.routines_db = TinyDB(routines_db_path)

    def action(self, spoken_text, arguments_list: list = []):
        self.bs.respond("Loading routines into database.")
        self.update_routines_database(
            self.routines_folder_path, self.routines_db)
        self.bs.respond("Successfully loaded routines into database.")

    def update_routines_database(self, routines_folder_path: str, routines_db):
        '''
        Scan the routines directory and update the routines database with
        routine files found. Any routines files removed from the directory
        will also be effectively removed from the routines database.
        '''
        # Remove old database and start with an empty one.
        routines_db.truncate()
        for file in os.scandir(routines_folder_path):
            if file.is_file() and file.path.endswith(".txt"):
                routine_name = ""
                print("file path is : ", file.path)
                with open(file.path, "r") as f:
                    # all routine files have the routine name as the first
                    # line.
                    routine_name = f.readline().splitlines()[0]
                Entry = Query()
                routine_details = {}
                routine_details["name"] = routine_name
                routine_details["filepath"] = file.path
                routines_db.upsert(
                    routine_details, Entry.name == routine_details["name"]
                )
