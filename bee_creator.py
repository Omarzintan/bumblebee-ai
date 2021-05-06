'''
This is a class responsible for spawning a bee (virtual assistant)
based on Bumblebee-Framework.
'''

import os
import yaml
from core import Bee
from utils.wake_word_detector import WakeWordDetector
from utils import config_builder
from utils import run_gracefully
from helpers import bumblebee_root
from features import feature_lists
from halo import Halo
import pyfiglet
import sys


class Bumblebee():
    def __init__(self, silent_mode=False,
                 name='bumblebee', config_yaml_name='config',
                 feature_list="all"):
        self.silent_mode = silent_mode
        self.name = name
        self.config_yaml_name = config_yaml_name
        self.feature_list = feature_lists.get(feature_list,
                                              feature_lists['all'])
        self.config = {}
        self.spinner = Halo(spinner='noise')
        self.wake_word_detector = WakeWordDetector(self.name)
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
            with open(bumblebee_root+"utils/" +
                      self.config_yaml_name+".yaml", "r") as ymlfile:
                self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)
                self.spinner.succeed()
        except FileNotFoundError:
            # %%
            # Build config file if it is not found.
            # -------------------------------------
            self.spinner.fail()
            self.spinner.start(text="Building configuration file.")
            if config_builder.build_yaml() == -1:  # pass name into build_yaml
                self.spinner.fail()
                raise Exception("Error building config file.")
            self.spinner.succeed(
                text="Configuration file built successfully at 'utils/" +
                self.config_yaml_name+".yaml'"
            )
            with open(bumblebee_root+"utils/" +
                      self.config_yaml_name+".yaml", "r") as ymlfile:
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
        virtual_assistant = Bee(
            self.name, self.feature_list, self.config, self.wake_word_detector)
        # bumblebee_api.set_bee_instance(virtual_assistant)
        return virtual_assistant

    def run_bee(self):
        '''
        Runs the instance of Bee we created in this class.
        '''
        while 1:
            try:
                name_banner = pyfiglet.figlet_format(self.name)
                print(name_banner)
                run_gracefully.start_gracefully(self.bee)
                if self.wake_word_detector.run():
                    self.bee.sleep = 0
                    print(self.bee.sleep)
                    # # will be replaced with our bumblebee_api command.
                    self.bee.run()
            except KeyboardInterrupt:
                run_gracefully.exit_gracefully(self.bee)
            except Exception:
                print(sys.exc_info())
                run_gracefully.exit_gracefully(
                    self.bee, crash_happened=True)
