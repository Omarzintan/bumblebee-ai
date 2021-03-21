from core import Bumblebee
import features
import sys, os
import json
import importlib

if __name__ == "__main__":
    
    print(features.__all__)
    
    # Update intents.json if features have been added/removed
    with open('features/intents.json', 'r') as json_data:
        intents = json.load(json_data)
        
    if len(features.__all__) != len(intents['intents']):
        print('Generating new intents.json file...')
        os.remove('features/intents.json')
        intents = {}
        intents['intents'] = []
        for feature in features.__all__:
            feature_object = importlib.import_module('features.'+feature, ".").Feature()
            tag = {}
            tag["tag"] = feature_object.tag_name
            tag["patterns"] = feature_object.patterns
            intents['intents'].append(tag)

        intents_json = json.dumps(intents, indent=2)
        
        with open('features/intents.json', 'w') as f:
            f.write(intents_json)
        
    bumblebee = Bumblebee(features.__all__)
    bumblebee.run()
