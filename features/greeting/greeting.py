#!python3

import random

greetings = [
    'Hey there!',
    'Wassup',
    'Yeo',
    'Hello',
    'How be?',
    'Good day.'
]

'''
Returns a random greeting.
Argument: <string> input
Return type: <string>
'''
def greet(input):
    return random.choice(greetings)
