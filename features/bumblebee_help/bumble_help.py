from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.keywords import Keywords
import pprint

class BumbleHelp(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        keywords = Keywords()
        response = """
        Hi i am Bumblebee, your virtual assistant.
        I can do many things such as telling the time, googling 
        information, doing math, and opening Youtube. I can also 
        clock you into work as well as track your browser activity
        in Google Chrome. Look at the list of commands to help.
        """
        list_of_commands = keywords.get('all')
        bs.respond(response)
        pprint.pprint(list_of_commands)
        return
