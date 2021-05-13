'''
This is a class responsible for spawning a bee (virtual assistant)
based on Bumblebee-Framework.
'''

import os
import yaml
from core import Bee
from utils.wake_word_detector import WakeWordDetector
from utils import config_builder
from helpers import bumblebee_root
from features import feature_lists
from halo import Halo
import pyfiglet


class Bumblebee():
    def __init__(self,
                 name='bumblebee', config_yaml_name='config',
                 feature_list_name="all"):
        self.name = name
        self.config_yaml_name = config_yaml_name
        self.feature_list = feature_lists.get(feature_list_name,
                                              feature_lists['all'])
        self.config = {}
        self.spinner = Halo(spinner='noise')
        self.wake_word_detector = WakeWordDetector(self.name)
        self.config_path = bumblebee_root+"utils/config/" + \
            self.config_yaml_name+".yaml"
        self.__preparation_step()
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
            # %%
            # Ensure that necessary directories exist.
            # ----------------------------------------
            self.spinner.start(
                text="Verifying existence of necessary folders.")
            database_path = self.config['Database']['path']
            research_files_path = self.config['Folders']['research_files']
            work_study_files_path = self.config['Folders']['work_study']
            models_path = self.config['Folders']['models']
            try:
                os.makedirs(database_path, exist_ok=True)
                os.makedirs(research_files_path, exist_ok=True)
                os.makedirs(work_study_files_path, exist_ok=True)
                os.makedirs(models_path, exist_ok=True)
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
