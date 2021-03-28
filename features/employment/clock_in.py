from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.employment import helpers
import features.global_vars as global_vars
import difflib
import datetime

class ClockIn(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

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
            helpers.clock_in(global_vars.employer, global_vars.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))

        elif 'osborn' in global_vars.employer:
            # access osborn file and put timestamp there
            global_vars.employer = 'osborn'
            global_vars.work_start_time = datetime.datetime.now()
            global_vars.currently_working = True
            helpers.clock_in(global_vars.employer, global_vars.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))
        bs.respond('You\'ve been clocked in for {}.'.format(global_vars.employer))
        return
