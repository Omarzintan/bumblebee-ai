from features.default import BaseFeature
import difflib
import datetime
import os
from tinydb import TinyDB
from helpers import bumblebee_root


class Constants:
    # Global Store Keys
    EMPLOYER = 'employer'
    WORK_START_TIME = 'work_start_time'
    DATETIME = 'datetime'
    CURRENTLY_WORKING = 'currently_working'


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "clock_in"
        self.patterns = ["clock in", "let's work", "start work", "clock me in"]
        super().__init__()

    def action(self, spoken_text):
        known_employers = self.get_employers()
        self.bs.respond('Which employer is this for?')
        print(f'List of employers: {known_employers}')

        self.globals_api.store(Constants.EMPLOYER, '')

        employer_text = self.bs.infinite_speaking_chances()

        if self.bs.interrupt_check(employer_text):
            return

        close_names = []
        while close_names == []:
            close_names = difflib.get_close_matches(
                employer_text, known_employers)
            if close_names == []:
                self.bs.respond(
                    'I don\'t know this employer. Please try again')

                self.globals_api.store(Constants.EMPLOYER, '')

                employer_text = self.bs.infinite_speaking_chances(
                    employer_text)

                if self.bs.interrupt_check(employer_text):
                    break

        # TODO: Is this step correct? Is close_names a list of lists?
        closest_matches = close_names[0]

        for employer in known_employers:
            # TODO: again this would probably only work if close_names is a list of lists?
            if employer in closest_matches:
                # TODO: put this into one object. Not sure if there is a strong reason for them to be separate
                self.globals_api.store(Constants.EMPLOYER, employer)
                self.globals_api.store(
                    Constants.WORK_START_TIME, datetime.datetime.now())
                self.globals_api.store(Constants.CURRENTLY_WORKING, True)

                # Log clock-in info into employer's file
                self.clock_in(
                    self.globals_api.retrieve(Constants.EMPLOYER),
                    self.globals_api.retrieve(Constants.WORK_START_TIME).strftime(
                        '%a %b %d, %Y %I:%M %p')
                )
                break

        self.bs.respond(
            'You\'ve been clocked in for {}.'.format(self.globals_api.retrieve(Constants.EMPLOYER)))
        return

    def clock_in(self, employer, work_start_time):
        '''
        Writes line in employer specific file saying I have logged in to work.
        Arguments: <string> employer name, <datetime.datetime object> work_start_time
        Return type: None
        '''
        # find/create employer file
        os.makedirs('work_study', exist_ok=True)
        with open(bumblebee_root+os.path.join('work_study', '{}_hours.txt'.format(employer)), 'a+') as file:
            file.write('Started work: {}\n'.format(work_start_time))

    def get_employers(self):
        '''
        Gets a list of all employers from the employer database.
        '''
        employer_db_path = self.config["Database"]["employers"]
        employer_db = TinyDB(employer_db_path)
        return [item["name"] for item in employer_db.all()]
