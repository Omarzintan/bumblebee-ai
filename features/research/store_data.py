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
            request, filename = helpers.store_data()
            bs.respond('Research data stored successfully at {}.txt'.format(filename))
            return
        except:
            print("Unexpected error:", sys.exc_info())
            bs.respond('Failed to store research data.')
            return
