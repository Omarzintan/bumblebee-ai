'''Default Feature Class'''
from core import Bumblebee

class BaseFeature(Bumblebee):
    tag_name = ''
    patterns = []

    def __init__(self):
        self.bs = self.speech
        self.index = None
        self.config = self.config_yaml
        
    def action(self, text):
        pass

    def set_index(self, value : int):
        self.index = value
