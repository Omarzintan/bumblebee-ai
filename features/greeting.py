#!python3
'''THIS IS DEPRECATED AND WILL BE REPLACED WITH A CHATBOT'''

from features.default import BaseFeature
import random


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "greeting"
        self.patterns = [
            "hello",
            "what's up",
            "hey",
            "are you there?",
            "anyone home?",
            "yo"
            ]
        super().__init__()

    def action(self, spoken_text):
        response = self.greet()
        self.bs.respond(response)
        return

    '''
    Returns a random greeting.
    Argument: None
    Return type: <string>
    '''
    def greet(self):
        greetings = [
            'Hey there!',
            'Wassup',
            'Yeo',
            'Hello',
            'How be?',
            'Good day.'
        ]
        return random.choice(greetings)
