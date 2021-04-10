import core
from core import Bumblebee
import features
import sys, os
import json
import importlib
import utils
import yaml
from utils import wake_word_detector

if __name__ == "__main__":
    # Access config file
    bumblebee_dir = ""
    config = ""
    try:
        with open("utils/config.yaml", "r") as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
            bumblebee_dir = config["Common"]["bumblebee_dir"]
    except FileNotFoundError:
        print("Please ensure that you have a config.yaml file in the utils direcroty")
        raise
        
    # Check to see that intents.json file exists.
    try:
        with open(bumblebee_dir+'/utils/intents.json', 'r') as json_data:
            intents = json.load(json_data)

        # Check whether any features have been added/removed.
        assert(len(features.__all__) == len(intents['intents']))
    except:
        # remove intents file if it exists        
        try:
            os.remove(bumblebee_dir+'utils/intents.json')
        except:
            print('intents.json file not found.')
            
        # Update intents.json if features have been added/removed or the file does not exist.
        print('Generating new intents.json file...')

        intents = {}
        intents['intents'] = []
        for x, feature in enumerate(features.__all__):
            # This way of importing is more friendly towards pyinstaller.
            feature_spec = importlib.util.spec_from_file_location("features."+feature, bumblebee_dir+"/features/"+feature+".py")
            feature_module = importlib.util.module_from_spec(feature_spec)
            feature_spec.loader.exec_module(feature_module)
            feature_object = feature_module.Feature()

            tag = {}
            tag["tag"] = feature_object.tag_name
            tag["patterns"] = feature_object.patterns
            tag["index"] = x
            intents['intents'].append(tag)

        intents_json = json.dumps(intents, indent=4)
        
        with open(bumblebee_dir+'/utils/intents.json', 'w') as f:
            f.write(intents_json)
        print('intents.json file generated.')
        
        # Retrain the NeuralNet
        print("Retraining NeuralNet...")
        exec(open("./train.py").read())
        print("NeuralNet trained.")
        

    while(1):
        try:
            bumblebee = Bumblebee(features.__all__, config)
            bumblebee.start_gracefully()
            if wake_word_detector.run():
                Bumblebee.sleep = 0                
                bumblebee.run()
        except IOError:
            bumblebee.exit_gracefully()
