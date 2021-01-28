from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
import datetime

class GetTime(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        strTime = datetime.datetime.now().strftime('%H:%M:%S')
        bs.respond(f'the time is {strTime}')
