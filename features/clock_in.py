from features.default import BaseFeature
from core import Bumblebee
import difflib
import datetime
import os
from helpers import bumblebee_root


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "clock_in"
        self.patterns = ["clock in", "let's work", "start work", "clock me in"]
        super().__init__()

    def action(self, spoken_text):
        self.bs.respond('Is this for Peggy or Osborn?')
        Bumblebee.employer = ''
        Bumblebee.employer = self.bs.infinite_speaking_chances(Bumblebee.employer)
        if self.bs.interrupt_check(Bumblebee.employer):
            return
        close_names = []
        while close_names == []:
            close_names = difflib.get_close_matches(Bumblebee.employer, ['peggy', 'osborn'])
            if close_names == []:
                self.bs.respond('I don\'t know this employer. Please try again')
                Bumblebee.employer = ''
                Bumblebee.employer = self.bs.infinite_speaking_chances(Bumblebee.employer)
                if self.bs.interrupt_check(Bumblebee.employer):
                    break

        Bumblebee.employer = close_names[0]
        if 'peggy' in Bumblebee.employer:
            Bumblebee.employer = 'peggy'
            Bumblebee.work_start_time = datetime.datetime.now()
            Bumblebee.currently_working = True
            # access peggy file and put timestamp there
            self.clock_in(Bumblebee.employer, Bumblebee.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))

        elif 'osborn' in Bumblebee.employer:
            # access osborn file and put timestamp there
            Bumblebee.employer = 'osborn'
            Bumblebee.work_start_time = datetime.datetime.now()
            Bumblebee.currently_working = True
            self.clock_in(Bumblebee.employer, Bumblebee.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))
        self.bs.respond('You\'ve been clocked in for {}.'.format(Bumblebee.employer))
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

