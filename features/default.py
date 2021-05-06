'''Contains default Feature class from which all other features inherit.'''
from core import Bee
from utils.globals_api import GLOBALSAPI


class BaseFeature(Bee):
    '''Default Feature Class'''
    tag_name = ''
    patterns = []

    def __init__(self):
        self.bs = self.speech
        self.index = None
        self.config = self.config_yaml
        self.globals_api = GLOBALSAPI()

    def action(self, text):
        pass

    def set_index(self, value: int):
        self.index = value
