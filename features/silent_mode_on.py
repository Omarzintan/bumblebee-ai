'''Turn on silent mode.'''
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "silent_mode_on"
        self.patterns = [
            "silent mode",
            "turn on silent mode",
            "start silent mode"
            ]
        super().__init__()

    def action(self, spoken_text):
        self.bs.respond('Okay. Starting silent mode.')
        self.bs.set_silent_mode(True)
        self.bs.respond('Welcome to silent mode.')
        return
