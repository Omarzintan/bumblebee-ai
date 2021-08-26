from features.default import BaseFeature
from rich.table import Table
from rich.console import Console
import time


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "bumble_help"
        self.patterns = [
            "tell me about yourself",
            "identify yourself",
            "help me",
            "I need help"
        ]
        self.api = bumblebee_api
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text, arguments_list: list = []):
        name = self.api.get_name()
        response = f"""
        Hi i am {name}, your virtual assistant.
        Look at the table of commands to see what I can do.
        """
        self.bs.respond(response)
        time.sleep(1)
        self.show_features()
        return

    def show_features(self):
        # get access to the intents file
        intents_json = self.api.get_intents()

        console = Console()

        table = Table(show_header=True, header_style="yellow")
        table.add_column("Feature")
        table.add_column("Patterns")
        for item in intents_json['intents']:
            tag = item['tag']
            patterns = item['patterns']
            table.add_row(tag, str(patterns))
        console.print(table)
