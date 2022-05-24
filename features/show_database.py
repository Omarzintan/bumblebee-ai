from tinydb import TinyDB
from rich.table import Table
from utils.console import console
from features.default import BaseFeature
from consolemenu import MultiSelectMenu, Screen
from consolemenu.items import FunctionItem


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "show_database"
        self.patterns = ["show database",
                         "show my database",
                         "display database", "reveal database"]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

    def action(self, spoken_text, arguments_list: list = []):
        # Create the root menu
        menu = MultiSelectMenu("Database Menu", "This is a Multi-Select Menu",
                               epilogue_text=(
                                   "Please select one or more entries "
                                   "separated by commas, and/or a range "
                                   "of numbers. For example:  1,2,3   or "
                                   "  1-4   or   1,3-4"),
                               exit_option_text='Close Databse Viewer')

        # Add all the items to the root menu
        menu.append_item(FunctionItem(
            "Contacts db", self.show_table, args=['contacts']))
        menu.append_item(FunctionItem(
            "Routines db", self.show_table, args=['routines']))
        menu.append_item(FunctionItem(
            "Employers db", self.show_table, args=['employers']))
        menu.append_item(FunctionItem(
            "Zoom db", self.show_table, args=['zoom']))
        menu.append_item(FunctionItem(
            "Research db", self.show_table, args=['research']))
        menu.append_item(FunctionItem(
            "All dbs", self.show_table, args=['all']))

        # Show the menu
        menu.start()
        menu.join()

    def create_db_tables(self, list_of_db_paths):
        '''
        Creates a rich table with db contents given a
        list of paths to tiny db's.
        '''
        list_of_tables = []
        for path in list_of_db_paths:
            db = TinyDB(path)
            db_name = path.split("/")[-1]
            table = Table(title=db_name)
            first_item = db.all()[0]
            for key in first_item.keys():
                table.add_column(key)
            for item in db:
                row = []
                for value in item.values():
                    row.append(str(value))
                # Need to unpack the tuple to be able to pass it
                # into add row. * does the unpacking.
                table.add_row(*tuple(row))
            list_of_tables.append(table)
        return list_of_tables

    def show_table(self, db_name):
        db_paths = []
        if db_name == 'all':
            db_paths = [
                self.config['Database']['contacts'],
                self.config['Database']['routines'],
                self.config['Database']['employers'],
                self.config['Database']['zoom'],
                self.config['Database']['research']
            ]
        else:
            db_paths = [self.config['Database'][db_name]]
        list_of_tables = self.create_db_tables(db_paths)
        for table in list_of_tables:
            console.print(table)
        Screen().input('Press [Enter] to continue')
