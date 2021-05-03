from features.default import BaseFeature
import difflib
import datetime
import os
from tinydb import TinyDB
from helpers import bumblebee_root


class StoreKeys:
    # Global Store Keys
    EMPLOYER = 'employer'
    WORK_START_TIME = 'work_start_time'
    CURRENTLY_WORKING = 'currently_working'


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "clock_in"
        self.patterns = ["clock in", "let's work", "start work", "clock me in"]
        super().__init__()

    def action(self, spoken_text):
        # TODO: what if user is already clocked in?
        known_employers = self.get_employers()
        self.bs.respond('Which employer is this for?')
        print(f'List of employers: {known_employers}')

        self.globals_api.store(StoreKeys.EMPLOYER, '')

        close_names = []
        while close_names == []:
            employer_text = self.bs.hear()

            if self.bs.interrupt_check(employer_text):
                return

            close_names = difflib.get_close_matches(
                employer_text, known_employers)

            if close_names == []:
                self.bs.respond(
                    'I don\'t know this employer. Please try again or cancel')

        found_employer = close_names[0]
        self.bs.respond('Should I clock you in for ' +
                        found_employer + '?')

        yes_words = ['yes', 'yea', 'yeah', 'ok', 'okay', 'sure']
        no_words = ['no', 'nope', 'nah']

        while True:
            yes_no_response = self.bs.hear()

            if yes_no_response in no_words or \
                    self.bs.interrupt_check(yes_no_response):
                self.bs.respond('Clock-in cancelled')
                break

            elif yes_no_response in yes_words:
                self.globals_api.store(StoreKeys.EMPLOYER, found_employer)
                self.globals_api.store(
                    StoreKeys.WORK_START_TIME, datetime.datetime.now())
                self.globals_api.store(StoreKeys.CURRENTLY_WORKING, True)

                # Log clock-in info into employer's file
                self.clock_in(
                    self.globals_api.retrieve(StoreKeys.EMPLOYER),
                    self.globals_api.retrieve(
                        StoreKeys.WORK_START_TIME).strftime(
                            '%a %b %d, %Y %I:%M %p'
                    )
                )

                self.bs.respond(
                    'You\'ve been clocked in for {}.'
                    .format(self.globals_api.retrieve(StoreKeys.EMPLOYER)))
                break
            else:
                self.bs.respond(
                    'Sorry, I did not get that. Please say yes, no or cancel.')

        return

    def clock_in(self, employer, work_start_time):
        '''
        Writes line in employer specific file saying I have logged in to work.
        Arguments: <string> employer name,
                   <datetime.datetime object> work_start_time
        Return type: None
        '''
        # find/create employer file
        os.makedirs('work_study', exist_ok=True)
        with open(
            bumblebee_root +
            os.path.join('work_study', '{}_hours.txt'.format(employer)), 'a+'
        ) as file:
            file.write('Started work: {}\n'.format(work_start_time))

    def get_employers(self):
        '''
        Gets a list of all employers from the employer database.
        '''
        employer_db_path = self.config["Database"]["employers"]
        employer_db = TinyDB(employer_db_path)
        return [item["name"] for item in employer_db.all()]
