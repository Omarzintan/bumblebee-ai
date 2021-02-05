from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars, helpers
import os, sys
import signal

class StopServer(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond('Stopping research server.')
        helpers.stop_server()
        return