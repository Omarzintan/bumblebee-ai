'''Default Feature Class'''

class BaseFeature():
    tag_name = ''
    patterns = []
    index = None

    def action(self, text):
        pass

    def set_index(self, value : int):
        self.index = value
