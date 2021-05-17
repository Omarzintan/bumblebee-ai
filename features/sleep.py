from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "sleep"
        self.patterns = ["I am done", "all done", "exit", "go to sleep", "bye"]
        self.api = bumblebee_api
        self.speech = self.api.get_speech()

    def action(self, spoken_text=''):
        self.speech.respond('Ok. I\'ll be listening for your command.')
        self.api.sleep_on()
        return
