'''Set the default speech mode.'''
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "set_default_speech_mode"
        self.patterns = [
            "save speech mode",
            "set default speech mode",
            "set default speech mode to",
            "set default speech mode as",
            "save default speech mode as"
        ]
        self.config = bumblebee_api.get_config()
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text, arguments_list: list = []):
        self.config["Utilities"]["default_speech_mode"] = self.bs.speech_mode
        self.bs.respond(f"Saved default speech mode as {self.bs.speech_mode}")
        # Write utility to help update the yaml file properly. For now,
        #  it does not work.
        # yaml file update will be handled by the bumblebee_api
        return
