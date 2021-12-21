'''Runs features based on tasks retrieved from online.'''
import requests
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "run_online_tasks"
        self.patterns = [
            "run online tasks"]
        self.api = bumblebee_api
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

    def action(self, spoken_text, arguments_list: list = []):
        # Get list of tasks from online api.
        try:
            response = requests.get(url="https://c9o8fm.deta.dev/commands")
            response_json = response.json()
            commands_list = response_json["commands"]
            if len(commands_list) == 0:
                self.bs.respond("There are no online tasks to run.")
                return
            # Run them using internal api.
            self.api.run_by_input_list(commands_list)
        except (requests.ConnectionError):
            self.bs.respond("No internet connection.")
