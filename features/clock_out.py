from features.default import BaseFeature
import datetime
import os

from features.clock_in import StoreKeys as clock_in_store_keys


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "clock_out"
        self.patterns = ["clock out", "done working",
                         "stop work", "clock me out of work"]
        self.api = bumblebee_api
        self.bs = self.api.get_speech()
        self.config = self.api.get_config()
        self.work_study_dir = self.config["Folders"]["work_study"]

    def action(self, spoken_text):
        is_currently_working = self.api.pop_var(
            clock_in_store_keys.CURRENTLY_WORKING)

        if not is_currently_working:
            self.bs.respond('You\'ve not been clocked in.')
            return

        work_start_time = self.api.pop_var(
            clock_in_store_keys.WORK_START_TIME)
        work_stop_time = datetime.datetime.now()
        duration = (work_stop_time - work_start_time)

        print('Duration: ', duration)
        self.clock_out(self.api.pop_var(clock_in_store_keys.EMPLOYER),
                       work_stop_time.strftime('%a %b %d, %Y %I:%M %p'),
                       duration)

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
        with open(os.path.join(
            self.work_study_dir, '{}_hours.txt'.format(employer)
        ), 'a+') as file:
            file.write('Ended work: {}\n'.format(work_stop_time))
            file.write('Duration: {}\n'.format(duration))
