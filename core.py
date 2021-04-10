'''The core of Bumblebee.'''
import importlib
from utils.speech import BumbleSpeech
import os
import sys
import json
import pickle
import datetime
import subprocess

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize



class Bumblebee():
    # global vars
    speech = BumbleSpeech()
    currently_working = False
    employer = ''
    work_start_time = ''
    research_server_proc = ''
    research_topic = ''
    sleep = 0
    crash_file = 'crash_recovery.p'
    crash_store = {}
    config_yaml = {}
    
    def __init__(self, features:list=[], config:dict={}):
        assert(config != {})
        Bumblebee.config_yaml = config
        self.bumblebee_dir = Bumblebee.config_yaml["Common"]["bumblebee_dir"]
        
        # %%
        # Building Feature objects from list of features.
        # -----------------------------------------------
        if features != []:
            self._features = []
            # Importing features this way is more friendly towards pyinstaller.
            for feature in features:
                spec = importlib.util.spec_from_file_location("features."+feature, self.bumblebee_dir+"features/"+feature+".py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module) # Without this line, module.Feature() in the next line will not work.
                self._features.append(module.Feature())

            self.feature_indices = {feature : x for x, feature in enumerate(features)}
        else:
            # Use default feature if no features are set.
            spec = importlib.util.spec_from_file_loaction("features.default", self.bumblebee_dir+"features/default.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self._features = [module.Feature()]
            self.feature_indices = {feature : x for x, feature in enumerate(self._features)}

        # %%
        # Accessing intents.json file.
        # ----------------------------
        try:
            # Check to see that intents.json file exists.
            with open(self.bumblebee_dir+'utils/intents.json', 'r') as json_data:
                intents = json.load(json_data)
            # Check whether any features have been added/removed.
            assert(len(self._features) == len(intents['intents']))
        except:
            # remove intents file if it exists        
            try:
                os.remove(self.bumblebee_dir+'utils/intents.json')
            except:
                print('intents.json file not found.')
            
            # Update intents.json if features have been added/removed or the file does not exist.
            print('Generating new intents.json file...')

            intents = {}
            intents['intents'] = []
            for x, feature in enumerate(self._features):
                tag = {}
                tag["tag"] = feature.tag_name
                tag["patterns"] = feature.patterns
                tag["index"] = x
                intents['intents'].append(tag)

            intents_json = json.dumps(intents, indent=4)
        
            with open(self.bumblebee_dir+'utils/intents.json', 'w') as f:
                f.write(intents_json)
            print('intents.json file generated.')

            # Retrain the NeuralNet
            print("Retraining NeuralNet...")
            output, errors = subprocess.Popen(['python', 'train.py'], stdout=subprocess.PIPE, text=True).communicate()
            print(output)
            print(errors)
            print("NeuralNet trained.")
            
    def run(self):
        # Prepping the Neural Net to be used.
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        with open('utils/intents.json', 'r') as json_data:
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

            tag_index = self.feature_indices[tag]
            self._features[tag_index].action(text)
        return
        
    """Get the config file that Bumblebee is running with."""
    def get_config(self):
        return self.config

    """
    FUNCTIONS NECESSARY FOR CRASH RECOVERY
    Crash recovery entails storing desired global variables in case
    a crash happens. So far, the employee info is stored and preserved 
    if the user is currently working. On reboot, the information about 
    much time has been spent working is restored. Also, if the research
    server process is running, it is killed before reboot happens.
    """
    def store_vars(self):
        Bumblebee.crash_store['work_start_time'] = Bumblebee.work_start_time
        Bumblebee.crash_store['currently_working'] = Bumblebee.currently_working
        Bumblebee.crash_store['employer'] = Bumblebee.employer
        with open(Bumblebee.crash_file, 'wb') as f:
            f.seek(0)
            pickle.dump(Bumblebee.crash_store, f)
        return
        
    def restore_vars(self):
        Bumblebee.crash_store = pickle.load(open(Bumblebee.crash_file, "rb"))
        Bumblebee.work_start_time = Bumblebee.crash_store['work_start_time']
        Bumblebee.currently_working = Bumblebee.crash_store['currently_working']
        Bumblebee.employer = Bumblebee.crash_store['employer']
        return

    def start_gracefully(self):
        try:
            if os.path.exists(Bumblebee.crash_file):
                print('Starting gracefully.')
                self.restore_vars()
                os.remove(Bumblebee.crash_file)
        except:
            print(sys.exc_info())
            print('Start gracefully failed.')
            pass
        return

    def exit_gracefully(self):
        print('Exiting gracefully.')
        if Bumblebee.research_server_proc:
            Bumblebee.speech.respond('Closing research server gracefully.')
            store_research_feature_index = self.feature_indices['store_research_data']
            stop_research_feature_index = self.feature_indices['stop_research_data']
            self._features[store_research_feature_index].action()
            self._features[stop_research_feature_index].action()
        if Bumblebee.currently_working:
            self.store_vars()
