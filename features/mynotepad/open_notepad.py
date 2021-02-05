from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.mynotepad import helpers

class OpenNotepad(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        helpers.notepad()
        return
    
