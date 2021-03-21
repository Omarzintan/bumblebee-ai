'''Default Feature Class'''
from core import Bumblebee

class BaseFeature():
    tag_name = ''
    patterns = []
    index = None
    bs = Bumblebee.speech

    def action(self, text):
        pass

    def set_index(self, value : int):
        self.index = value
