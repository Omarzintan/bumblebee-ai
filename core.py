'''The core of Bumblebee.'''
import importlib
from utils.speech import BumbleSpeech

import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize



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
        # Prepping the Neural Net to be used.
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        with open('features/intents.json', 'r') as json_data:
            intents = json.load(json_data)

        FILE = "models/data.pth"
        data = torch.load(FILE)

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data["all_words"]
        tags = data["tags"]
        model_state = data["model_state"]

        model = NeuralNet(input_size, hidden_size, output_size).to(device)
        model.load_state_dict(model_state)
        model.eval()

        
        self.speech.respond('Hey.')
        self.speech.respond('How may I help you?')

        while(self.sleep == 0):
            action_found = False
            text = ''
            text = self.speech.infinite_speaking_chances(text)

            text = tokenize(text)
            x = bag_of_words(text, all_words)
            x = x.reshape(1, x.shape[0])
            x = torch.from_numpy(x).to(device)

            output = model(x)
            _, predicted = torch.max(output, dim=1)

            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            if prob.item() < 0.70:
                self.speech.respond("I do not understand...")
                self.sleep = 1
                continue

            print(f"tag: {tag}")
            '''
            for feature in self._features:
                print('feature: ', feature)
                print('tag_name: ',feature.tag_name)
                print('patterns: ',feature.patterns)
                print('index: ', feature.index)
            '''
        return
