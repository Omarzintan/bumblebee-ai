'''Generates a random password and copies it to the clipboard.'''
from features.default import BaseFeature
import pyperclip as pc
import secrets
import string


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "password_generator"
        self.patterns = [
            "create password", "create a password",
            "give me a password", "make a password",
            "make a random password"
        ]
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text, arguments_list: list = []):
        password_length = 18
        password = "".join([secrets.choice(
            string.digits + string.ascii_letters + string.punctuation)
            for _ in range(password_length)])
        pc.copy(password)
        self.bs.respond(
            "I have copied the generated password to your clipboard. "
            "Use ctrl+v to paste it wherever."
        )
        return
