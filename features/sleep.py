from features.default import BaseFeature
from core import Bumblebee

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "sleep"
        self.patterns = ["I am done", "all done", "exit", "go to sleep", "bye"]

    def action(self, spoken_text=''):
        self.bs.respond('Ok. I\'ll be listening for your command.')
        Bumblebee.sleep = 1
        return
