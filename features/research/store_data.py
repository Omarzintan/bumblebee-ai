from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars, helpers
import requests
import os, sys

class StoreData(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        try:
            filename = glocal_vars.research_topic
            filename = filename.replace(' ', '-')
            res = requests.post(os.getenv('SERVER_URL')+'/store_data', params={'filename': filename})
            res.raise_for_status()
            bs.respond('Research data stored successfully at {}.txt'.format(filename))
            return
        except:
            print("Unexpected error:", sys.exc_info())
            bs.respond('Failed to store research data.')
            return
