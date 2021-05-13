'''Contains default Feature class from which all other features inherit.'''


class BaseFeature():
    '''Default Feature Class'''
    tag_name = ''
    patterns = []

    def __init__(self, bumblebee_api):
        self.index = None
        self.bumblebee_api = bumblebee_api
        self.config = self.bumblebee_api.get_config()
        self.bs = self.bumblebee_api.get_speech()

    def action(self, text):
        pass

    def set_index(self, value: int):
        self.index = value
