from features.default import BaseFeature
from core import Bumblebee
import difflib
import datetime
import os
from tinydb import TinyDB
from helpers import bumblebee_root


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "clock_in"
        self.patterns = ["clock in", "let's work", "start work", "clock me in"]
        super().__init__()

    def action(self, spoken_text):
        employers = self.get_employers()
        self.bs.respond('Which employer is this for?')
        print(f'List of employers: {employers}')
        Bumblebee.employer = ''
        Bumblebee.employer = self.bs.infinite_speaking_chances(Bumblebee.employer)
        if self.bs.interrupt_check(Bumblebee.employer):
            return
        close_names = []
        while close_names == []:
            close_names = difflib.get_close_matches(Bumblebee.employer, employers)
            if close_names == []:
                self.bs.respond('I don\'t know this employer. Please try again')
                Bumblebee.employer = ''
                Bumblebee.employer = self.bs.infinite_speaking_chances(Bumblebee.employer)
                if self.bs.interrupt_check(Bumblebee.employer):
                    break

        Bumblebee.employer = close_names[0]
        for employer in employers:
            if employer in Bumblebee.employer:
                Bumblebee.employer = employer
                Bumblebee.work_start_time = datetime.datetime.now()
                Bumblebee.currently_working = True
                # access peggy file and put timestamp there
                self.clock_in(Bumblebee.employer, Bumblebee.work_start_time.strftime('%a %b %d, %Y %I:%M %p'))
                break
            
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

    '''
    Gets a list of all employers from the employer database.
    '''
    def get_employers(self):
        employer_db_path = self.config["Database"]["employers"]
        employer_db = TinyDB(employer_db_path)
        return [item["name"] for item in employer_db.all()]
