'''Default Feature Class'''
from core import Bumblebee
from configparser import ConfigParser, ExtendedInterpolation
import yaml

class BaseFeature():
    tag_name = ''
    patterns = []

    def __init__(self):
        self.bs = Bumblebee.speech
        self.index = None
#        self.config = ConfigParser(interpolation=ExtendedInterpolation())
#        self.config.read('utils/config.ini')
        try:
            with open("utils/config.yaml", "r") as ymlfile:
                self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("Config file not found.")
        
    def action(self, text):
        pass

    def set_index(self, value : int):
        self.index = value
