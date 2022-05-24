from features.default import BaseFeature
import os
from features.feature_helpers import markdown_viewer


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = 'display_research_file'
        self.patterns = [
            "show my research",
            "display my research",
            "show research",
            "display research",
            "open research file"
        ]
        self.api = bumblebee_api
        self.bs = self.api.get_speech()
        self.config = self.api.get_config()

    def action(self, spoken_text: str = "", arguments_list: list = []):
        try:
            research_topic = self.bs.ask_question(
                "What is the topic of the file you want to open?")
            research_files_path = self.config['Folders']['research_files']
            filename = research_topic.replace(' ', '-')
            filepath = os.path.join(research_files_path, filename+".md")
            markdown_viewer(filepath)
            return
        except Exception as exception:
            print(exception)
            return
