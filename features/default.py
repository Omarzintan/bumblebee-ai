'''Default Feature Class'''
from core import Bumblebee
from configparser import ConfigParser, ExtendedInterpolation

class BaseFeature():
    tag_name = ''
    patterns = []

    def __init__(self):
        self.bs = Bumblebee.speech
        self.index = None
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read('utils/config.ini')
        
    def action(self, text):
        pass

    def set_index(self, value : int):
        self.index = value
