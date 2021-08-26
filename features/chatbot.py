from features.default import BaseFeature
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "chatbot"
        self.patterns = [
            "are you there?",
            "anyone home?",
            "let's chat",
            "what is"
        ]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()
        chatbot_db_path = self.config["Database"]["chatbot"]

        if not os.path.exists(chatbot_db_path):
            self.chatbot = ChatBot(
                'Bumblebee',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'threshold': 0.70,
                        'default_response': 'Sorry, I do not understand'
                    },
                    'chatterbot.logic.MathematicalEvaluation'
                ],
                database_uri='sqlite:///'+chatbot_db_path
            )
            trainer = ChatterBotCorpusTrainer(self.chatbot)
            trainer.train("chatterbot.corpus.english")

        else:
            self.chatbot = ChatBot(
                'Bumblebee',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'threshold': 0.70,
                        'default_response': 'Sorry, I do not understand'
                    },
                    'chatterbot.logic.MathematicalEvaluation'
                ],
                database_uri='sqlite:///'+chatbot_db_path
            )

    def action(self, spoken_text, arguments_list: list = []):
        response = self.chatbot.get_response(' '.join(spoken_text))
        self.bs.respond(str(response))
        return
