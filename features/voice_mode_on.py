'''Turn off silent mode.'''
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "voice_mode_on"
        self.patterns = [
            "turn on voice mode",
            "voice mode",
            "voice mode on",
            "start voice mode"
        ]
        super().__init__()

    def action(self, spoken_text):
        self.bs.set_speech_mode('voice')
        self.bs.respond('Welcome to voice mode.')
        return