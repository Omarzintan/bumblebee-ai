#!python3
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
import random

class Greeting(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond(self.greet())
        return


    '''
    Returns a random greeting.
    Argument: None
    Return type: <string>
    '''
    def greet():
        greetings = [
            'Hey there!',
            'Wassup',
            'Yeo',
            'Hello',
            'How be?',
            'Good day.'
        ]
        return random.choice(greetings)
