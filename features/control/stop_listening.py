from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features import global_vars
from features import wake_word_detector
from features.research import helpers as research_help
from features.research import glocal_vars as research_glocal

class StopListening(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond('To get me back you will have to boot me back up. Are you sure?')
        approve = ''
        approve = bs.infinite_speaking_chances(approve)
        if bs.interrupt_check(approve):
            return
        if 'yes' in approve:
            bs.respond('See you later then, bye. Take care.')
            if research_glocal.server_proc:
                research_help.stop_server()
            if global_vars.currently_working:
                work_stop_time = datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
                duration = str(int(work_stop_time) - int(global_vars.work_start_time)).strftime('%H:%M:%S')
                employment.clock_out(global_vars.employer, work_stop_time, duration)
            wake_word_detector.stop()
        else:
            bs.respond('Alright, I will not stop.')
            return
