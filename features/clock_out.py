from features.default import BaseFeature
import datetime
import os
from core import Bumblebee
from helpers import bumblebee_root


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "clock_out"
        self.patterns = ["clock out", "done working", "stop work", "clock me out of work"]
        super().__init__()

    def action(self, spoken_text=''):
        if not Bumblebee.currently_working:
            self.bs.respond('You\'ve not been clocked in.')
            return
        
        work_stop_time = datetime.datetime.now()
        duration = (work_stop_time - Bumblebee.work_start_time)
        print('Duration: ', duration)
        self.clock_out(Bumblebee.employer, work_stop_time.strftime('%a %b %d, %Y %I:%M %p'), duration)
        self.bs.respond('You\'ve been clocked out.')
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

