'''Set the default speech mode.'''
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "set_default_speech_mode"
        self.patterns = [
            "save speech mode",
            "set default speech mode",
            "set default speech mode to",
            "set default speech mode as",
            "save default speech mode as"
        ]
        super().__init__()

    def action(self, spoken_text):
        self.config["Utilities"]["default_speech_mode"] = self.bs.speech_mode
        self.bs.respond(f"Saved default speech mode as {self.bs.speech_mode}")
        # Write utility to help update the yaml file properly. For now,
        #  it does not work.
        return
