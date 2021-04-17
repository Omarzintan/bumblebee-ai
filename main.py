import os
import yaml
import features
from core import Bumblebee
from utils import wake_word_detector
from utils import config_builder
from utils import run_gracefully
from helpers import bumblebee_root

if __name__ == "__main__":

    config = {}
    try:
        # %%
        # Access config file
        # ------------------
        print("Accessing configuration file")
        with open(bumblebee_root+"utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except FileNotFoundError:
        # %%
        # Build config file if it is not found.
        # -------------------------------------
        print("Building configuration file.")
        if config_builder.build_yaml() == -1:
            raise Exception("Error building config file.")
        print("Configuration file built successfully at 'utils/config.yaml'")
        with open("utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    finally:
        # %%
        # Ensure that necessary directories exist.
        # ----------------------------------------
        print("Verifying existence of necessary folders.")
        database_path = config['Database']['path']
        research_files_path = config['Folders']['research_files']
        work_study_files_path = config['Folders']['work_study']
        try:
            os.makedirs(database_path, exist_ok=True)
            os.makedirs(research_files_path, exist_ok=True)
            os.makedirs(work_study_files_path, exist_ok=True)
            print("All necessary folders exist.")
        except OSError as exception:
            raise OSError(exception)

    while 1:
        try:
            bumblebee = Bumblebee(features.__test__, config)
            run_gracefully.start_gracefully()
            if wake_word_detector.run():
                Bumblebee.sleep = 0
                bumblebee.run()
        except IOError:
            CRASH_HAPPENED = True
            run_gracefully.exit_gracefully(bumblebee, CRASH_HAPPENED)
        except KeyboardInterrupt:
            run_gracefully.exit_gracefully(bumblebee)
