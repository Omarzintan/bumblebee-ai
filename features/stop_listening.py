from utils import run_gracefully
from features.default import BaseFeature
from features import clock_out


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "stop_listening"
        self.patterns = ["stop listening", "shutdown", "shut down"]
        super().__init__()

    def action(self, spoken_text=''):
        self.bs.respond('To get me back you will have to boot me back up. Are you sure?')
        approve = ''
        approve = self.bs.infinite_speaking_chances(approve)
        if self.bs.interrupt_check(approve):
            return
        if 'yes' in approve:
            currently_working = self.globals_api.retrieve("currently_working")
            if currently_working:
                clock_out.Feature().action()
            self.bs.respond('See you later then, bye. Take care.')
            raise KeyboardInterrupt('Exiting Bumblebee')
        else:
            self.bs.respond('Alright, I will not stop.')
            return
