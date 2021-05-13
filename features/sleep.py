from features.default import BaseFeature
from core import Bee


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "sleep"
        self.patterns = ["I am done", "all done", "exit", "go to sleep", "bye"]
        super().__init__()

    def action(self, spoken_text=''):
        self.bs.respond('Ok. I\'ll be listening for your command.')
        Bee.sleep = 1
        return
