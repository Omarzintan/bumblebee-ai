'''Contains default Feature class from which all other features inherit.'''


class BaseFeature():
    '''Default Feature Class'''
    tag_name = ''
    patterns = []

    def __init__(self, bumblebee_api):
        pass

    # Note that features the Bee.py class run function tokenizes text before
    # passing it to features. So features receive text in a tokenized form.
    def action(self, text):
        pass

    def set_index(self, value: int):
        self.index = value
