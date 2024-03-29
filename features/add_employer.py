from features.default import BaseFeature
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
            self.term_add_employer_details()
            self.bs.respond('Added new employer successfully.')
        except Exception as exception:
            print(exception)
            self.bs.respond('Could not add new employer.')

        return

    def term_add_employer_details(self):
        '''
        Allows the user to enter employer info through the terminal.
        '''
        name = self.bs.ask_question("Please enter a name for the employer:")
        if not name:
            return
        Entry = Query()
        employer_details = {}
        employer_details["name"] = name.lower()
        self.employer_db.upsert(
            employer_details, Entry.name == employer_details["name"]
        )
