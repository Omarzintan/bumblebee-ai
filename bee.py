'''The core code of the virtual assistant.'''
import importlib
import os
import json
import torch

from utils.speech import BumbleSpeech
from utils.bumblebee_internal_api import BUMBLEBEEAPI
from utils.wake_word_detector import WakeWordDetector
from halo import Halo
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from utils.run_gracefully import GracefulRunner
from train import IntentsTrainer


class Bee():

    def __init__(self,
                 name: str = 'bumblebee',
                 features: list = ['default'],
                 config: dict = {},
                 wake_word_detector: WakeWordDetector = None,
                 default_speech_mode: str = 'voice'):
        self.name = name
        self.wake_word_detector = wake_word_detector
        self.speech = BumbleSpeech(speech_mode=default_speech_mode)
        self.graceful_runner = GracefulRunner(self)
        self.intents_filename = 'intents-'+self.name

        assert config != {}
        self.config_yaml = config

        self.bumblebee_dir = self.config_yaml["Common"]["bumblebee_dir"]
        self.python3_path = self.config_yaml["Common"]["python3_path"]
        self.models_path = self.config_yaml["Folders"]["models"]
        self.trained_model_path = self.models_path+self.name+".pth"
        self.intents_file_path = self.bumblebee_dir + \
            'utils/intents/'+self.intents_filename+'.json'

        self.spinner = Halo(spinner='dots2')

        self.bumblebee_api = BUMBLEBEEAPI(self)
        self.sleep = 0
        self.thread_failsafes = []
        self.global_store = {}

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
                self._features.append(module.Feature(self.bumblebee_api))

            self.feature_indices = {feature: x for x,
                                    feature in enumerate(features)}

        # %%
        # Accessing intents.json file.
        # ----------------------------
        try:
            # Check to see that intents.json file exists.
            with open(
                self.intents_file_path, 'r'
            ) as json_data:
                intents_json = json.load(json_data)
            # Check whether any features have been added/removed or if
            # no trained model is present.
            assert(len(self._features) == len(intents_json['intents']))
            assert(os.path.exists(self.trained_model_path))
        except (FileNotFoundError, AssertionError):
            # remove intents file if it exists
            try:
                print('Detected modification in feature list.')
                os.remove(self.intents_file_path)
            except OSError:
                print('intents.json file not found.')

            # Update intents.json if features have been added/removed
            # or the file does not exist.
            self.spinner.start(text='Generating new intents json file...')

            intents = {}
            intents['intents'] = []
            for x, feature in enumerate(self._features):
                tag = {}
                tag["tag"] = feature.tag_name
                tag["patterns"] = feature.patterns
                tag["index"] = x
                intents['intents'].append(tag)

            intents_json = json.dumps(intents, indent=4)

            with open(self.intents_file_path, 'w') as f:
                f.write(intents_json)
            self.spinner.succeed(
                text=f'{self.intents_file_path} file generated.')

            self.trainer = IntentsTrainer(
                self.intents_file_path, model_name=self.name)
            # Retrain the NeuralNet
            self.spinner.start(text='Training NeuralNet.')
            self.trainer.train()
            self.spinner.succeed('NeuralNet trained.')

        finally:
            # Save the intents json file
            self.intents_json = intents_json

            # Prepping the Neural Net to be used.
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')

            self.model_data = torch.load(self.trained_model_path)

            input_size = self.model_data["input_size"]
            hidden_size = self.model_data["hidden_size"]
            output_size = self.model_data["output_size"]
            self.all_words = self.model_data["all_words"]
            self.tags = self.model_data["tags"]
            self.model_state = self.model_data["model_state"]

            self.model = NeuralNet(input_size, hidden_size,
                                   output_size).to(self.device)
            self.model.load_state_dict(self.model_state)
            self.model.eval()

    def run(self):
        '''Main function that runs Bumblebee'''
        while 1:
            if self.speech.speech_mode == self.speech.speech_modes[1]:
                try:
                    self.graceful_runner.start_gracefully()
                    if self.wake_word_detector.run():
                        self.sleep = 0
                        self.take_command()
                except KeyboardInterrupt:
                    self.graceful_runner.exit_gracefully()
                except Exception as exception:
                    print(exception)
                    self.graceful_runner.exit_gracefully(
                        crash_happened=True)
            elif self.speech.speech_mode == self.speech.speech_modes[0]:
                try:
                    self.sleep = 0
                    self.take_command()
                except KeyboardInterrupt:
                    self.graceful_runner.exit_gracefully()
                except Exception as exception:
                    print(exception)
                    self.graceful_runner.exit_gracefully(
                        crash_happened=True)

    def take_command(self):
        """
        Function for running features given input from user.
        """
        while(self.sleep == 0):
            text = ''
            text = self.speech.hear()

            text = tokenize(text)
            x = bag_of_words(text, self.all_words)
            x = x.reshape(1, x.shape[0])
            x = torch.from_numpy(x).to(self.device)

            output = self.model(x)
            _, predicted = torch.max(output, dim=1)

            tag = self.tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            if prob.item() < 0.80:
                tag_index = self.feature_indices['chatbot']
                self._features[tag_index].action(text)
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
        '''Get the config file that Bee is running with.'''
        return self.config_yaml

    def get_speech(self):
        '''Get the BumbleSpeech instance.'''
        return self.speech

    def get_intents(self):
        '''Get the intents json file Bee is running with.'''
        return self.intents_json

    def get_internal_state(self):
        return {
            'sleep': self.sleep,
            'global_store': self.global_store,
            'thread_failsafes': self.thread_failsafes
        }

    def load_internal_state(self, state={}):
        if not isinstance(state, dict):
            raise Exception('Invalid argument, state. Must be a dict')

        self.sleep = state.get('sleep', 0)
        self.thread_failsafes = state.get('thread_failsafes', [])
        self.global_store = state.get('global_store', {})
