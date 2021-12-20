'''Turn on silent mode.'''
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "silent_mode_on"
        self.patterns = [
            "silent mode on",
            "turn on silent mode",
            "start silent mode",
            "silent mode"
        ]
        self.speech = bumblebee_api.get_speech()

    def action(self, spoken_text, arguments_list: list = []):
        self.speech.respond('Okay. Starting silent mode.')
        self.speech.set_speech_mode('silent')
        self.speech.respond('Welcome to silent mode.')
        return
