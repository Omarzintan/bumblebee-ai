'''Default Feature Class'''
from core import Bumblebee

class BaseFeature():
    tag_name = ''
    patterns = []

    def __init__(self):
        self.bs = Bumblebee.speech
        self.index = None

    def action(self, text):
        pass

    def set_index(self, value : int):
        self.index = value
