'''
This is a class responsible for spawning a bee (virtual assistant).
'''

import os
import yaml
from bee import Bee
from utils.wake_word_detector import WakeWordDetector
from utils import config_builder
from helpers import bumblebee_root
from features import feature_lists
from halo import Halo
import pyfiglet


class BumblebeeWrapper():
    def __init__(self,
                 name='bumblebee', config_yaml_name='config',
                 feature_list_name="all"):
        self.config_yaml_name = config_yaml_name
        self.config = {}
        self.spinner = Halo(spinner='noise')
        self.config_path = os.path.join(bumblebee_root, "utils/config/",
                                        self.config_yaml_name+".yaml")
        self.__preparation_step()
        self.name = self.config["Preferences"]["wake_phrase"]
        feature_list_name = self.config["Preferences"]["feature_list"]
        self.feature_list = feature_lists.get(feature_list_name,
                                              feature_lists['all'])
        self.wake_word_detector = WakeWordDetector(self.name)
        self.bee = self.__create_bee()

    def __preparation_step(self):
        '''
        Steps to prepare for the creation of a virtual assistant.
        '''
        try:
            # %%
            # Access config file
            # ------------------
            self.spinner.start(text="Accessing configuration file")
            with open(self.config_path, "r") as ymlfile:
                self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)
                self.spinner.succeed()
        except FileNotFoundError:
            # %%
            # Build config file if it is not found.
            # -------------------------------------
            self.spinner.fail()
            self.spinner.start(text="Building configuration file.")
            # Ensure that config folder exists
            os.makedirs(os.path.join(bumblebee_root,
                        "utils", "config"), exist_ok=True)
            if config_builder.build_yaml(self.config_path) == -1:
                self.spinner.fail()
                raise Exception("Error building config file.")
            self.spinner.succeed(
                text="Configuration file built successfully at 'utils/" +
                self.config_yaml_name+".yaml'"
            )
            with open(self.config_path, "r") as ymlfile:
                self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)
        finally:
            self.name = self.config["Preferences"]["wake_phrase"]
            # %%
            # Ensure that necessary directories exist.
            # ----------------------------------------
            self.spinner.start(
                text="Verifying existence of necessary folders.")
            database_path = self.config['Database']['path']
            try:
                os.makedirs(database_path, exist_ok=True)
                for folder_path in self.config["Folders"]:
                    os.makedirs(folder_path, exist_ok=True)
                self.spinner.succeed(text="All necessary folders exist.")
            except OSError as exception:
                self.spinner.fail()
                raise OSError(exception)

    def __create_bee(self):
        '''
        Creates an instansce of Bee with name, feature_list and a config file.
        '''
        # access default mode from config file
        default_speech_mode = self.config["Utilities"]["default_speech_mode"]
        virtual_assistant = Bee(
            self.name, self.feature_list,
            self.config, self.wake_word_detector, default_speech_mode)
        return virtual_assistant

    def run_bee(self):
        '''
        Runs the instance of Bee we created in this class.
        '''
        name_banner = pyfiglet.figlet_format(self.name)
        print(name_banner)
        self.bee.run()
