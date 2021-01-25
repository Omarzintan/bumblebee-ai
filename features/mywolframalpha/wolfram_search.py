from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from database import wolframalpha_key as wak
import wolframalpha

class WolframalphaSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        for word in self.keywords:
            spoken_text = spoken_text.replace(word, '')
        app_id = wak.get_key()
        client = wolframalpha.Client(app_id)
        try:
            res = client.query(spoken_text)
            answer = next(res.results).text
            bs.respond('The answer is ' + answer)
        except:
            try:
                answer = wikipedia.summary(question, sentences = 2)
                bs.respond('According to Wikipedia')
                bs.respond(answer)
            except:
                bs.respond('Sorry I could not perform your search.')
