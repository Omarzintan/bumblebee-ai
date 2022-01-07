'''
This is a class responsible for spawning a bee (virtual assistant).
'''

import os
import yaml
from bee import Bee
from utils.wake_word_detector import WakeWordDetector
from utils import config_builder, env
from helpers import bumblebee_root, spinner, log_user_in, get_api_key
from features import feature_lists
import pyfiglet


class BumblebeeWrapper():
    def __init__(self,
                 # TODO: use decision_strategy, name, as defaults if no config
                 name='bumblebee',
                 config_yaml_name='config',
                 feature_list_name="all",
                 decision_strategy="rule-based"):
        self.config_yaml_name = config_yaml_name
        self.config = {}
        self.config_path = os.path.join(bumblebee_root, "utils/config/",
                                        self.config_yaml_name+".yaml")
        self.__preparation_step()
        self.name = self.config["Preferences"]["wake_phrase"]
        feature_list_name = self.config["Preferences"]["feature_list"]
        self.feature_list = feature_lists.get(feature_list_name,
                                              feature_lists['all'])
        self.decision_strategy = self.config[
            "Preferences"]["decision_strategy"]
        self.wake_word_detector = WakeWordDetector(self.name)
        self.bee = self.__create_bee()

    def __preparation_step(self):
        '''
        Steps to prepare for the creation of a virtual assistant.
        '''
        try:
            # Access config file
            # ------------------
            spinner.start(text="Accessing configuration file")
            with open(self.config_path, "r") as ymlfile:
                self.config = yaml.load(ymlfile)
                # TODO: add exception to catch if the config file is
                # corrupted/not of the right shape/vital configs are missing
                spinner.succeed()
        except FileNotFoundError:
            # Build config file if it is not found.
            # -------------------------------------
            spinner.fail()
            spinner.start(text="Building configuration file.")
            # Ensure that config folder exists
            os.makedirs(os.path.join(bumblebee_root,
                                     "utils", "config"), exist_ok=True)
            if config_builder.build_yaml(self.config_path) == -1:
                spinner.fail()
                raise Exception("Error building config file.")
            spinner.succeed(
                text="Configuration file built successfully at 'utils/" +
                self.config_yaml_name+".yaml'"
            )
            with open(self.config_path, "r") as ymlfile:
                self.config = yaml.load(ymlfile)
        finally:
            self.name = self.config["Preferences"]["wake_phrase"]
            # Ensure that necessary directories exist.
            # ----------------------------------------
            spinner.start(
                text="Verifying existence of necessary folders.")
            database_path = self.config['Database']['path']
            try:
                os.makedirs(database_path, exist_ok=True)
                for folder_path in self.config["Folders"]:
                    os.makedirs(self.config["Folders"]
                                [folder_path], exist_ok=True)
                spinner.succeed(text="All necessary folders exist.")
            except OSError as exception:
                spinner.fail()
                raise OSError(exception)
            # Check that Bumblebee API key exists.
            # ----------------------------------------
            spinner.start("Checking existence of Bumblebee token.")
            existing_api_key = self.config.get(
                'Api_keys', {}).get('bumblebee_online', None)

            if existing_api_key:
                spinner.succeed(text="Found Bumblebee token.")
            else:
                spinner.fail(text="Bumblebee token not found.")
                jwt_token = log_user_in()
                if jwt_token:
                    spinner.start(text="Getting api key from online server.")

                    api_key = get_api_key(jwt_token)

                    if not api_key:
                        spinner.fail(text="Could not download api key.")
                    else:
                        # set api key in config and update config
                        config_builder.update_yaml(
                            self.config_path,
                            ['Api_keys', 'bumblebee_online'],
                            api_key)

                        spinner.succeed(
                            text="Api key successfully downloaded.")

    def __create_bee(self):
        '''
        Creates an instance of Bee with name, feature_list and a config file.
        '''
        # access default speech mode from config file
        default_speech_mode = self.config["Utilities"]["default_speech_mode"]

        virtual_assistant = Bee(
            name=self.name,
            features=self.feature_list,
            config=self.config,
            wake_word_detector=self.wake_word_detector,
            default_speech_mode=default_speech_mode,
            decision_strategy=self.decision_strategy
        )
        return virtual_assistant

    def run_bee(self):
        '''
        Runs the instance of Bee we created in this class.
        '''
        name_banner = pyfiglet.figlet_format(self.name)
        print(name_banner)
        spinner.succeed("Decision Strategy: " + self.decision_strategy)
        spinner.succeed('Environment: ' + env.environment)
        self.bee.run()
