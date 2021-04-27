'''The core of Bumblebee.'''
import importlib
import os
import json
import subprocess
import torch

from utils.speech import BumbleSpeech
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize


class Bumblebee():
    # global vars
    speech = BumbleSpeech()
    config_yaml = {}
    sleep = 0
    global_store = {
        "currently_working": False,
        "employer": '',
        "work_start_time": '',
        "research_server_proc": '',
        "research_topic": '',
        "threads": []
        }

    def __init__(self, features: list = ['default'], config: dict = {}):
        assert config != {}
        Bumblebee.config_yaml = config
        self.bumblebee_dir = Bumblebee.config_yaml["Common"]["bumblebee_dir"]
        self.python3_path = Bumblebee.config_yaml["Common"]["python3_path"]

        # %%
        # Building Feature objects from list of features.
        # -----------------------------------------------
        if features != []:
            self._features = []
            # Importing features this way is more friendly towards pyinstaller.
            for feature in features:
                spec = importlib.util.spec_from_file_location(
                    "features." + feature, self.bumblebee_dir +
                    "features/" + feature+".py"
                )
                module = importlib.util.module_from_spec(spec)
                # Without this line, module.Feature() in the next line
                # will not work.
                spec.loader.exec_module(module)
                self._features.append(module.Feature())

            self.feature_indices = {feature: x for x, feature in enumerate(features)}

        # %%
        # Accessing intents.json file.
        # ----------------------------
        try:
            # Check to see that intents.json file exists.
            with open(self.bumblebee_dir+'utils/intents.json', 'r') as json_data:
                intents = json.load(json_data)
            # Check whether any features have been added/removed.
            assert(len(self._features) == len(intents['intents']))
        except (FileNotFoundError, AssertionError):
            # remove intents file if it exists
            try:
                os.remove(self.bumblebee_dir+'utils/intents.json')
            except OSError:
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
            output, errors = subprocess.Popen(
                [self.python3_path, self.bumblebee_dir+'train.py'],
                stdout=subprocess.PIPE,
                text=True
            ).communicate()
            print(output)
            print(errors)
            print("NeuralNet trained.")

    def run(self):
        """
        Main function for running features given input from user.
        """
        # Prepping the Neural Net to be used.
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        FILE = self.bumblebee_dir+"models/data.pth"
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

        while(self.sleep == 0):
            text = ''
            text = self.speech.hear()

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

    def run_by_tags(self, feature_tags: list):
        '''Run a list of features given their tags.'''
        if len(feature_tags) > 0:
            for tag in feature_tags:
                try:
                    tag_index = self.feature_indices[tag]
                    self._features[tag_index].action("")
                except KeyError:
                    if not tag_index:
                        print(f"Could not find feature index of {tag}.")
                    else:
                        print(f"Could not perform action for {tag}")

    def get_config(self):
        '''Get the config file that Bumblebee is running with.'''
        return self.config_yaml
