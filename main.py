from core import Bumblebee
import features
import sys, os
import json
import importlib
import train

if __name__ == "__main__":
    # Check to see that intents.json file exists.
    try:
        with open('features/intents.json', 'r') as json_data:
            intents = json.load(json_data)
        assert(len(features.__all__) == len(intents['intents']))
    except:
        # remove file if it exists        
        try:
            os.remove('features/intents.json')
        except:
            print('intents.json file not found.')
            
        # Update intents.json if features have been added/removed or the file does not exist.        
        print('Generating new intents.json file...')

        intents = {}
        intents['intents'] = []
        for x, feature in enumerate(features.__all__):
            feature_object = importlib.import_module('features.'+feature, ".").Feature()
            tag = {}
            tag["tag"] = feature_object.tag_name
            tag["patterns"] = feature_object.patterns
            tag["index"] = x
            intents['intents'].append(tag)

        intents_json = json.dumps(intents, indent=4)
        
        with open('features/intents.json', 'w') as f:
            f.write(intents_json)

        # Retrain the NeuralNet
        print("Retraining NeuralNet...")
        train.train()
        
    bumblebee = Bumblebee(features.__all__)
    bumblebee.run()
