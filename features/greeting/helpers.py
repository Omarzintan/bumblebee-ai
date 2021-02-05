from features.greeting import glocal_vars
import random

'''
Returns a random greeting.
Argument: <string> input
Return type: <string>
'''
def greet(input):
    return random.choice(glocal_vars.greetings)
