from tinydb import TinyDB
from rich.table import Table
from utils.console import console
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "show_database"
        self.patterns = ["show database",
                         "show my database",
                         "display database", "reveal database"]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

    def action(self, spoken_text, arguments_list: list = []):
        try:
            # get all database paths.
            db_paths = [
                self.config['Database']['contacts'],
                self.config['Database']['routines'],
                self.config['Database']['employers'],
                self.config['Database']['zoom'],
                self.config['Database']['research']]
            list_of_tables = self.create_db_tables(db_paths)
            for table in list_of_tables:
                console.print(table)
        except Exception as exception:
            print(exception)
        return

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
