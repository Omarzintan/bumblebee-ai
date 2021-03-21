from features.default import BaseFeature
from features.global_vars import bumble_speech as bs
from features.employment import helpers
import features.global_vars as global_vars
import difflib
import datetime
import os
from helpers import bumblebee_root


class Feature(BaseFeature):
    def __init__(self, keywords):
        self.tag_name = "clock_in"
        self.patterns = ["clock in", "lets work", "start work", "clock me in"]
        self.index

    def action(self, spoken_text):
        bs.respond('Is this for Peggy or Osborn?')
        global_vars.employer = ''
        global_vars.employer = bs.infinite_speaking_chances(global_vars.employer)
        if bs.interrupt_check(global_vars.employer):
            return
        close_names = []
        while close_names == []:
            close_names = difflib.get_close_matches(global_vars.employer, ['peggy', 'osborn'])
            if close_names == []:
                bs.respond('I don\'t know this employer. Please try again')
                global_vars.employer = ''
                global_vars.employer = bs.infinite_speaking_chances(global_vars.employer)
                if bs.interrupt_check(global_vars.employer):
                    break

        global_vars.employer = close_names[0]
        if 'peggy' in global_vars.employer:
            global_vars.employer = 'peggy'
            global_vars.work_start_time = datetime.datetime.now()
            global_vars.currently_working = True
            # access peggy file and put timestamp there
            self.clock_in(global_vars.employer, global_vars.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))

        elif 'osborn' in global_vars.employer:
            # access osborn file and put timestamp there
            global_vars.employer = 'osborn'
            global_vars.work_start_time = datetime.datetime.now()
            global_vars.currently_working = True
            self.clock_in(global_vars.employer, global_vars.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))
        bs.respond('You\'ve been clocked in for {}.'.format(global_vars.employer))
        return

    '''
    Writes line in employer specific file saying I have logged in to work.
    Arguments: <string> employer name, <datetime.datetime object> work_start_time
    Return type: None
    '''
    def clock_in(self, employer, work_start_time):
        # find/create employer file
        os.makedirs('work_study', exist_ok=True)
        with open(bumblebee_root+os.path.join('work_study', '{}_hours.txt'.format(employer)), 'a+') as file:
            file.write('Started work: {}\n'.format(work_start_time))

