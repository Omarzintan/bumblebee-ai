from utils.speech import BumbleSpeech
from utils.bumblebee_internal_api import BUMBLEBEEAPI
from utils import config_builder
from utils.helpers import bumblebee_root


class MockBee():
    def __init__(self,
                 name: str = 'mock bumblebee',
                 ):
        self.name = name
        self.speech = BumbleSpeech(speech_mode="silent")
        self.bumblebee_dir = bumblebee_root
        self.bumblebee_api = BUMBLEBEEAPI(self)
        self.thread_failsafes = []
        self.global_store = {}
        self.config = config_builder.create_fake_config()

    def run_feature(self, feature, input):
        return feature.action

    def get_speech(self):
        return self.speech

    def get_config(self):
        return self.config

    def get_internal_state(self):
        return {
            'global_store': self.global_store,
            'thread_failsafes': self.thread_failsafes
        }

    def load_internal_state(self, state={}):
        if not isinstance(state, dict):
            raise Exception('Invalid argument, state. Must be a dict')
