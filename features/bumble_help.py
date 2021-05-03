from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "bumble_help"
        self.patterns = [
            "tell me about yourself",
            "identify yourself",
            "who are you?",
            "what are you?"]
        super().__init__()

    def action(self, spoken_text):
        response = """
        Hi i am Bumblebee, your virtual assistant.
        I can do many things such as telling the time, googling
        information, doing math, and opening Youtube. I can also
        clock you into work as well as track your browser activity
        in Google Chrome. Look at the list of commands to help.
        """
        self.bs.respond(response)
        return
