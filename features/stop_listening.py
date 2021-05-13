from features.default import BaseFeature


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "stop_listening"
        self.patterns = ["stop listening", "shutdown", "shut down"]
        self.api = bumblebee_api
        self.speech = self.api.get_speech()

    def action(self, spoken_text=''):
        self.speech.respond(
            'To get me back you will have to boot me back up. Are you sure?'
        )
        approve = self.speech.hear()
        if self.speech.interrupt_check(approve):
            return
        if 'yes' in approve:
            currently_working = self.api.get_var("currently_working")
            if currently_working:
                self.api.run_by_tags(['clock_out'])
            self.speech.respond('See you later then, bye. Take care.')
            raise KeyboardInterrupt('Exiting Bumblebee')
        else:
            self.speech.respond('Alright, I will not stop.')
            return
