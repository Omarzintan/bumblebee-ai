from features.default import BaseFeature
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "chatbot"
        self.patterns = []
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()
        chatbot_db_path = self.config["Database"]["chatbot"]

        if not os.path.exists(chatbot_db_path):
            self.chatbot = ChatBot(
                'Bumblebee',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///'+chatbot_db_path
            )
            trainer = ChatterBotCorpusTrainer(self.chatbot)
            trainer.train("chatterbot.corpus.english")

        else:
            self.chatbot = ChatBot(
                'Bumblebee',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///'+chatbot_db_path
            )

    def action(self, spoken_text, arguments_list: list = []):
        if isinstance(spoken_text, list):
            spoken_text = ' '.join(spoken_text)
        print("Spoken text:" + spoken_text)
        response = self.chatbot.get_response(spoken_text)
        self.bs.respond(str(response))
        return
