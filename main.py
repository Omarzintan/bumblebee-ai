import os
import yaml
import features
from core import Bumblebee
from utils import wake_word_detector
from utils import config_builder
from utils import run_gracefully
from helpers import bumblebee_root
from halo import Halo
import sys

if __name__ == "__main__":

    config = {}
    spinner = Halo(spinner='noise')
    try:
        # %%
        # Access config file
        # ------------------
        spinner.start(text="Accessing configuration file")
        with open(bumblebee_root+"utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
            spinner.succeed()
    except FileNotFoundError:
        # %%
        # Build config file if it is not found.
        # -------------------------------------
        spinner.fail()
        spinner.start(text="Building configuration file.")
        if config_builder.build_yaml() == -1:
            spinner.fail()
            raise Exception("Error building config file.")
        spinner.succeed(
            text="Configuration file built successfully at 'utils/config.yaml'"
        )
        with open(bumblebee_root+"utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    finally:
        # %%
        # Ensure that necessary directories exist.
        # ----------------------------------------
        spinner.start(text="Verifying existence of necessary folders.")
        database_path = config['Database']['path']
        research_files_path = config['Folders']['research_files']
        work_study_files_path = config['Folders']['work_study']
        models_path = config['Folders']['models']
        try:
            os.makedirs(database_path, exist_ok=True)
            os.makedirs(research_files_path, exist_ok=True)
            os.makedirs(work_study_files_path, exist_ok=True)
            os.makedirs(models_path, exist_ok=True)
            spinner.succeed(text="All necessary folders exist.")
        except OSError as exception:
            spinner.fail()
            raise OSError(exception)

    while 1:
        try:
            bumblebee = Bumblebee(features.__all__, config)
            run_gracefully.start_gracefully()
            if wake_word_detector.run():
                Bumblebee.sleep = 0
                bumblebee.run()
        except KeyboardInterrupt:
            run_gracefully.exit_gracefully(bumblebee)
        except:
            print(sys.exc_info())
            run_gracefully.exit_gracefully(bumblebee, crash_happened=True)
