#!python3
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.greeting import glocal_vars, helpers

class Greeting(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond(helpers.greet(spoken_text))
        return
