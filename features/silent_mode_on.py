'''Turn on silent mode.'''
from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "silent_mode_on"
        self.patterns = [
            "silent mode on",
            "turn on silent mode",
            "start silent mode",
        ]
        super().__init__(bumblebee_api)

    def action(self, spoken_text):
        self.bs.respond('Okay. Starting silent mode.')
        self.bs.set_speech_mode('silent')
        self.bs.respond('Welcome to silent mode.')
        # TODO
        # use bumblebee_api to exit out of while loop for voice mode,
        # change the speech mode to silent and then call the run function again
        # same for switching to voice mode.
        return
