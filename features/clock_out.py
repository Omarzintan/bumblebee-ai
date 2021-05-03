from features.default import BaseFeature
import datetime
import os
from helpers import bumblebee_root

from features.clock_in import StoreKeys as clock_in_store_keys


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "clock_out"
        self.patterns = ["clock out", "done working",
                         "stop work", "clock me out of work"]
        super().__init__()

    def action(self, spoken_text):
        is_currently_working = self.globals_api.retrieve(
            clock_in_store_keys.CURRENTLY_WORKING)

        if not is_currently_working:
            self.bs.respond('You\'ve not been clocked in.')
            return

        work_start_time = self.globals_api.retrieve(
            clock_in_store_keys.WORK_START_TIME)
        work_stop_time = datetime.datetime.now()
        duration = (work_stop_time - work_start_time)

        print('Duration: ', duration)
        self.clock_out(self.globals_api.retrieve(clock_in_store_keys.EMPLOYER),
                       work_stop_time.strftime('%a %b %d, %Y %I:%M %p'),
                       duration)

        # Clear store values related to work
        self.globals_api.store(clock_in_store_keys.EMPLOYER, '')
        self.globals_api.store(clock_in_store_keys.CURRENTLY_WORKING, False)
        self.globals_api.store(clock_in_store_keys.WORK_START_TIME, '')

        self.bs.respond('You\'ve been clocked out.')
        return

    '''
    Writes line in employer specific file saying I have logged out of work.
    Arguments: <string> employer name,
               <datetime.datetime object> work_stop_time,
               <datetime.timedelta object> duration
    Return type: None
    '''

    def clock_out(self, employer, work_stop_time, duration):
        # find/create employer file
        os.makedirs('work_study', exist_ok=True)
        with open(bumblebee_root+os.path.join(
            'work_study', '{}_hours.txt'.format(employer)
        ), 'a+') as file:
            file.write('Ended work: {}\n'.format(work_stop_time))
            file.write('Duration: {}\n'.format(duration))
