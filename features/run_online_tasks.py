'''Runs features based on tasks retrieved from online.'''
import requests
from features.default import BaseFeature
from utils.constants import BUMBLEBEE_ONLINE_GET_COMMANDS_URL


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "run_online_tasks"
        self.patterns = [
            "run online tasks"]
        self.api = bumblebee_api
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

    def action(self, spoken_text, arguments_list: list = []):
        # Get api key
        api_key = ""
        try:
            api_key = self.config["Api_keys"]["bumblebee_online"]
        except KeyError:
            # TODO: allow user to log in right here and continue as normal
            self.bs.respond(
                "Could not access token from config.\n" +
                "Please restart bumblebee and login to use this feature.")
            return

        # Get list of tasks from online api.
        try:
            headers = {"api_key": api_key}
            response = requests.get(
                url=BUMBLEBEE_ONLINE_GET_COMMANDS_URL, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                commands_list = response_json["commands"]
                if len(commands_list) == 0:
                    self.bs.respond("There are no online tasks to run.")
                    return
                # Run them using internal api.
                self.api.run_by_input_list(commands_list)
                return
            self.bs.respond(
                f"Could not run online commands due to error code \
                {response.status_code}.")
        except (requests.ConnectionError):
            self.bs.respond("Failed to connect to online server.")
