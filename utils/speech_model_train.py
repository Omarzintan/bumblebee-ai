# train.py
import json
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from utils.nltk_utils import bag_of_words, tokenize, stem
from utils.model import NeuralNet
from utils.helpers import bumblebee_root


class IntentDataset(Dataset):

    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


class IntentsTrainer():
    def __init__(self, intents_file_path, model_name='data'):
        self.model_name = model_name
        with open(intents_file_path, 'r') as f:
            intents = json.load(f)

        self.all_words = []
        self.tags = []
        self.xy = []
        self.x_train = []
        self.y_train = []
        # loop through each sentence in intents patterns
        for intent in intents['intents']:
            tag = intent['tag']
            self.tags.append(tag)
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = tokenize(pattern)
                # add to our words list
                self.all_words.extend(w)
                # add to xy pair
                self.xy.append((w, tag))

        # stem and lower each word
        ignore_words = ['?', '.', '!']
        self.all_words = [stem(w)
                          for w in self.all_words if w not in ignore_words]
        # remove duplicates and sort
        self.all_words = sorted(set(self.all_words))
        self.tags = sorted(set(self.tags))

    def create_training_data(self):
        # create training data

        for (pattern_sentence, tag) in self.xy:
            # x: bag of words for each pattern sentence
            bag = bag_of_words(pattern_sentence, self.all_words)
            self.x_train.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = self.tags.index(tag)
            self.y_train.append(label)

        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)

    def train(self):
        # create_training_data first
        self.create_training_data()

        # Hyper-parameters
        num_epochs = 800
        batch_size = 8
        learning_rate = 0.001
        input_size = len(self.x_train[0])
        hidden_size = 8
        output_size = len(self.tags)

        dataset = IntentDataset(self.x_train, self.y_train)
        train_loader = DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=True,
                                  num_workers=2)
        # if using Python3.8, set num_workers=0. Python3.8 has a spawn vs
        # fork issue that causes this to fail if num_workers > 0

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = NeuralNet(input_size, hidden_size, output_size).to(device)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        # Train the model
        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                words = words.to(device)
                labels = labels.to(device)

                # Forward pass
                outputs = model(words)
                # if y would be one-hot, we must apply
                # labels = torch.max(labels, 1)[1]
                loss = criterion(outputs, labels)

                # Backwards and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch+1) % 100 == 0:
                print(
                    f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

        print(f'final loss: {loss.item():.4f}')

        data = {
            "model_state": model.state_dict(),
            "input_size": input_size,
            "hidden_size": hidden_size,
            "output_size": output_size,
            "all_words": self.all_words,
            "tags": self.tags
        }

        FILE = bumblebee_root+"models/"+self.model_name+".pth"
        torch.save(data, FILE)

        print(f'training complete. file saved to {FILE}')
