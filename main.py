from core import Bumblebee
import features
import yaml
from utils import wake_word_detector
from utils import config_builder

if __name__ == "__main__":
   
    config = {}
    try:
        # %%
        # Access config file
        # ------------------
        print("Accessing configuration file")
        with open("utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except FileNotFoundError:
        # %%
        # Build config file if it is not found.
        # -------------------------------------
        print("Building configuration file.")
        if config_builder.build_yaml() == -1:
            raise("Error building config file.")
        print("Configuration file built successfully at 'utils/config.yaml'")
        with open("utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    while(1):
        try:
            bumblebee = Bumblebee(features.__all__, config)
            bumblebee.start_gracefully()
            if wake_word_detector.run():
                Bumblebee.sleep = 0                
                bumblebee.run()
        except IOError:
            bumblebee.exit_gracefully()
