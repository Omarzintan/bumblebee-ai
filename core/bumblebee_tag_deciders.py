import json
import os
from utils.nltk_utils import bag_of_words, tokenize
import torch
from utils.model import NeuralNet

from utils.speech_model_train import IntentsTrainer
from utils.helpers import spinner


class TagDecider:
    def decide(self):
        pass


class NeuralNetworkTagDecider(TagDecider):
    def __init__(self,
                 intents_file_path=None,
                 trained_model_path=None,
                 features=None,
                 model_name=None
                 ):
        super().__init__()

        self.intents_file_path = intents_file_path
        self.trained_model_path = trained_model_path
        self.model_name = model_name
        self.features = features if features else []
        self.intents_json = None

        # Accessing intents.json file.
        # ----------------------------
        try:
            # Check to see that intents.json file exists.
            with open(
                self.intents_file_path, 'r'
            ) as json_data:
                intents_json = json.load(json_data)

            # Check whether any features have been added/removed or if
            # no trained model is present.
            assert(len(self.features) == len(intents_json['intents']))
            assert(os.path.exists(self.trained_model_path))
        except (FileNotFoundError, AssertionError):
            # remove intents file if it exists
            try:
                print('Detected modification in feature list.')
                os.remove(self.intents_file_path)
            except OSError:
                print('intents.json file not found.')

            # Update intents.json if features have been added/removed
            # or the file does not exist.
            spinner.start(text='Generating new intents json file...')

            intents = {}
            intents['intents'] = []
            for x, feature in enumerate(self.features):
                tag = {}
                tag["tag"] = feature.tag_name
                tag["patterns"] = feature.patterns
                tag["index"] = x
                intents['intents'].append(tag)

            intents_json = json.dumps(intents, indent=4)

            with open(self.intents_file_path, 'w') as f:
                f.write(intents_json)
            spinner.succeed(
                text=f'{self.intents_file_path} file generated.')

            self.trainer = IntentsTrainer(
                self.intents_file_path, model_name=self.model_name)
            # Retrain the NeuralNet
            spinner.start(text='Training NeuralNet.')
            self.trainer.train()
            spinner.succeed('NeuralNet trained.')

        finally:
            # Save the intents json file
            self.intents_json = intents_json

            # Prepping the Neural Net to be used.
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')

            self.model_data = torch.load(self.trained_model_path)

            input_size = self.model_data["input_size"]
            hidden_size = self.model_data["hidden_size"]
            output_size = self.model_data["output_size"]
            self.all_words = self.model_data["all_words"]
            self.tags = self.model_data["tags"]
            self.model_state = self.model_data["model_state"]

            self.model = NeuralNet(input_size, hidden_size,
                                   output_size).to(self.device)
            self.model.load_state_dict(self.model_state)
            self.model.eval()

    def decide(self, spoken_text):
        """
        This function utilizes a neural network to determine
        which feature to run based on the input text.

        See for More: https://www.techwithtim.net/tutorials/ai-chatbot/
        """
        text = tokenize(spoken_text)
        x = bag_of_words(text, self.all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x).to(self.device)

        output = self.model(x)
        _, predicted = torch.max(output, dim=1)

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        predicted_tag = self.tags[predicted.item()]
        predicted_tag_probability = prob.item()

        # if no accurate action is found from
        # spoken_text, default to chatbot feature.
        tag = predicted_tag if predicted_tag_probability >= 0.8 else 'chatbot'
        return tag


class RuleBasedTagTagDecider(TagDecider):
    def __init__(self, features=None) -> None:
        super().__init__()

        self.features = features if features else []

    def decide(self, spoken_text: str):
        """
        This function decides which features to run from the given
        text input without using a neural network. All the logic
        here works based on rules.
        """
        tag = 'chatbot'
        spoken_text = spoken_text.lower()

        def is_matching_feature(feature):
            return any(phrase in spoken_text for phrase in feature.patterns)

        for feature in self.features:
            if is_matching_feature(feature):
                tag = feature.tag_name
                break

        return tag
