from features.default import BaseFeature
from core import Bumblebee
from utils import wake_word_detector
from features import clock_out
from features import store_research_data
from features import stop_research_server

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
            if Bumblebee.currently_working:
                clock_out.Feature().action()
            if Bumblebee.research_server_proc:
                store_research_data.Feature().action()
                stop_research_server.Feature().action()
            self.bs.respond('See you later then, bye. Take care.')                
            wake_word_detector.stop()
        else:
            self.bs.respond('Alright, I will not stop.')
            return
