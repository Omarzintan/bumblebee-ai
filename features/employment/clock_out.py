from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.employment import helpers
import features.global_vars as global_vars
import datetime


class ClockOut(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        if not global_vars.currently_working:
            respond('You\'ve not been clocked in.')
            return
        global_vars.currently_working = False
        work_stop_time = datetime.datetime.now()
        duration = (work_stop_time - global_vars.work_start_time)
        print(duration)
        helpers.clock_out(global_vars.employer, work_stop_time.strftime('%d-%m-%Y, %H:%M:%S'), duration)
        bs.respond('You\'ve been clocked out.')
        return
