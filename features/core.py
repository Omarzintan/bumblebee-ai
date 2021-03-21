'''The core of Bumblebee.'''
import importlib
from features.speech import BumbleSpeech

class Bumblebee():
    def __init__(self, features:list=[]):
        # define global vars here
        self.speech = BumbleSpeech()
        self.currently_working = False
        self.employer = ''
        self.work_start_time = ''
        self.sleep = 0
        
        if features != []:
            self._features = [
                importlib.import_module('features.'+feature, ".").Feature() for feature in features]
            for x, feature in enumerate(self._features):
                feature.set_index(x)

        else:
            # Use default feature if no features are set.
            self._features = [ importlib.import_module('features.default', ".").Feature()]

    def run(self):
        self.speech.respond('Hey.')
        self.speech.respond('How may I help you?')

        while(self.sleep == 0):
            action_found = False
            text = ''
            text = self.speech.infinite_speaking_chances(text)

            for feature in self._features:
                print(feature)
        return

