from features.default import BaseFeature
from rich.table import Table
from utils.console import console
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
        list_of_features = self.api.get_features()

        table = Table(show_lines=True, show_header=True,
                      title="List of Bumblebee features",
                      header_style="yellow")
        table.add_column("Feature")
        table.add_column("Patterns")
        for feature in list_of_features:
            tag = feature.tag_name
            patterns = feature.patterns
            table.add_row(tag, ', '.join(patterns))
        console.print(table)
