from features.default import BaseFeature
from features.global_vars import bumble_speech as bs
from features.keywords import Keywords
import pprint

class Feature(BaseFeature):
    def __init__(self, keywords):
        self.tag_name = "help"
        self.patterns = ["tell me about yourself", "identify yourself", "who are you?", "what are you?"]
        self.index

    def action(self, spoken_text):
        keywords = Keywords()
        response = """
        Hi i am Bumblebee, your virtual assistant.
        I can do many things such as telling the time, googling 
        information, doing math, and opening Youtube. I can also 
        clock you into work as well as track your browser activity
        in Google Chrome. Look at the list of commands to help.
        """
        list_of_commands = keywords.get('all') # THIS WILL NEED TO CHANGE
        bs.respond(response)
        pprint.pprint(list_of_commands)
        return
