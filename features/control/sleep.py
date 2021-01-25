from features.features import BaseFeature
from features.global_vars import bumble_speech as bs

class Sleep(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond('Ok. I\'ll be listening for your command.')
        return
