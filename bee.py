'''The core code of the virtual assistant.'''
from itertools import zip_longest
from utils.run_gracefully import GracefulRunner
from utils.wake_word_detector import WakeWordDetector
from utils.bumblebee_internal_api import BUMBLEBEEAPI
from utils.speech import BumbleSpeech
import importlib
import os
from utils.bumblebee_tag_deciders \
    import NeuralNetworkTagDecider, \
    RuleBasedTagTagDecider


class Bee():

    def __init__(self,
                 name: str = 'bumblebee',
                 features: list = ['default'],
                 config: dict = {},
                 decision_strategy: str = 'rule-based',
                 wake_word_detector: WakeWordDetector = None,
                 default_speech_mode: str = 'voice'):
        self.name = name
        self.wake_word_detector = wake_word_detector
        self.speech = BumbleSpeech(speech_mode=default_speech_mode)
        self.graceful_runner = GracefulRunner(self)
        self.intents_filename = 'intents-'+self.name

        self.tag_decider = None

        assert config != {}
        self.config_yaml = config

        self.bumblebee_dir = self.config_yaml["Common"]["bumblebee_dir"]
        self.python3_path = self.config_yaml["Common"]["python3_path"]
        self.models_path = self.config_yaml["Folders"]["models"]
        self.intents_folder_path = self.config_yaml["Folders"]["intents"]
        self.trained_model_path = os.path.join(
            self.models_path, self.name+".pth")
        self.intents_file_path = os.path.join(
            self.intents_folder_path, self.intents_filename+'.json')

        self.bumblebee_api = BUMBLEBEEAPI(self)
        self.sleep = 0
        self.thread_failsafes = []
        self.global_store = {}

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

            if decision_strategy == 'neural-network':
                self.tag_decider = NeuralNetworkTagDecider(
                    intents_file_path=self.intents_file_path,
                    trained_model_path=self.trained_model_path,
                    features=self._features,
                    model_name=self.name)
            elif decision_strategy == 'rule-based':
                self.tag_decider = RuleBasedTagTagDecider(
                    features=self._features)
            else:
                raise Exception('Could not find decision strategy')

    def run(self):
        '''Main function that runs Bumblebee'''
        while 1:
            # Voice mode
            if self.speech.speech_mode == self.speech.speech_modes[1]:
                try:
                    self.graceful_runner.start_gracefully()
                    if self.wake_word_detector.run():
                        self.take_and_run_command()
                except KeyboardInterrupt:
                    self.graceful_runner.exit_gracefully()
                except Exception as exception:
                    print(exception)
                    self.graceful_runner.exit_gracefully(
                        crash_happened=True)
            # Silent mode
            elif self.speech.speech_mode == self.speech.speech_modes[0]:
                try:
                    self.take_and_run_command()
                except KeyboardInterrupt:
                    self.graceful_runner.exit_gracefully()
                except Exception as exception:
                    print(exception)
                    self.graceful_runner.exit_gracefully(
                        crash_happened=True)

    def run_by_tags(self, feature_tags: list, arguments_list: list = []):
        '''Run a list of features given their tags and arguments.'''
        tags_with_arguments = zip_longest(
            feature_tags, arguments_list, fillvalue=[])
        for tag_argument_tuple in list(tags_with_arguments):
            try:
                tag = tag_argument_tuple[0]
                arguments = tag_argument_tuple[1]
                tag_index = self.feature_indices[tag]
                self._features[tag_index].action("", arguments)
            except KeyError:
                if not tag_index:
                    self.speech.respond(
                        f"Could not find feature index of {tag}.")
                else:
                    self.speech.respond(
                        f"Could not perform action for {tag}")

    def run_by_input_list(self, input_list: list):
        """
        Runs actions as infered from a list of commands.
        """
        tag = None
        for input in input_list:
            tag = self.tag_decider.decide(input)
            tag_index = self.feature_indices[tag]
            self._features[tag_index].action(input)

    def take_and_run_command(self):
        """
        Gets user input and executes feature action that matches
        the decided tag.
        """
        self.sleep = 0
        while(self.sleep == 0):
            text = ''
            text = self.speech.hear()
            tag = self.tag_decider.decide(text)
            tag_index = self.feature_indices[tag]
            self._features[tag_index].action(text)

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
