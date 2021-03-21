from features.default import BaseFeature
from features.global_vars import bumble_speech as bs
from features.employment import helpers
import features.global_vars as global_vars
import datetime
import os
from helpers import bumblebee_root


class Feature(BaseFeature):
    def __init__(self, keywords):
        self.tag_name = "clock_out"
        self.patterns = ["clock out", "done working", "stop work", "clock me out of work"]
        self.index

    def action(self, spoken_text):
        if not global_vars.currently_working:
            bs.respond('You\'ve not been clocked in.')
            return
        global_vars.currently_working = False
        work_stop_time = datetime.datetime.now()
        duration = (work_stop_time - global_vars.work_start_time)
        print('Duration: ', duration)
        self.clock_out(global_vars.employer, work_stop_time.strftime('%a %b %d, %Y %I:%M %p'), duration)
        bs.respond('You\'ve been clocked out.')
        return

    '''
    Writes line in employer specific file saying I have logged out of work.
    Arguments: <string> employer name, <datetime.datetime object> work_stop_time, <datetime.timedelta object> duration
    Return type: None
    '''        
    def clock_out(employer, work_stop_time, duration):
        # find/create employer file
        os.makedirs('work_study', exist_ok=True)
        with open(bumblebee_root+os.path.join('work_study', '{}_hours.txt'.format(employer)), 'a+') as file:
            file.write('Ended work: {}\n'.format(work_stop_time))
            file.write('Duration: {}\n'.format(duration))

