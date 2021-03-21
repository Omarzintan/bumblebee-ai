'''The core of Bumblebee.'''
import importlib
from utils.speech import BumbleSpeech

class Bumblebee():
    # define global vars here
    speech = BumbleSpeech()
    currently_working = False
    employer = ''
    work_start_time = ''
    sleep = 0
    
    def __init__(self, features:list=[]):
            
        if features != []:
            self._features = [
                importlib.import_module('features.'+feature, ".").Feature() for feature in features]
            for x, feature in enumerate(self._features):
                feature.set_index(x)

        else:
            # Use default feature if no features are set.
            self._features = [ importlib.import_module('features.default', ".").Feature()]

    def run(self):
        #self.speech.respond('Hey.')
        #self.speech.respond('How may I help you?')

        while(self.sleep == 0):
            action_found = False
            #text = ''
            #text = self.speech.infinite_speaking_chances(text)

            for feature in self._features:
                print('feature: ', feature)
                print('tag_name: ',feature.tag_name)
                print('patterns: ',feature.patterns)
                print('index: ', feature.index)
            self.sleep = 1
        return

