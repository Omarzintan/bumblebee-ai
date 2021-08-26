from features.default import BaseFeature
import difflib
import datetime
import os
from tinydb import TinyDB


class StoreKeys:
    # Global Store Keys
    EMPLOYER = 'employer'
    WORK_START_TIME = 'work_start_time'
    CURRENTLY_WORKING = 'currently_working'


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "clock_in"
        self.patterns = ["clock in", "let's work", "start work", "clock me in"]
        self.api = bumblebee_api
        self.config = self.api.get_config()
        self.bs = self.api.get_speech()
        self.work_study_dir = self.config["Folders"]["work_study"]

    def action(self, spoken_text, arguments_list: list = []):
        # TODO: what if user is already clocked in?
        known_employers = self.get_employers()
        self.bs.respond('Which employer is this for?')
        print(f'List of employers: {known_employers}')

        self.api.store_var(StoreKeys.EMPLOYER, '')

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
        if self.bs.approve(f'Should I clock you in for {found_employer}?'):
            self.api.store_var(StoreKeys.EMPLOYER, found_employer)
            self.api.store_var(
                StoreKeys.WORK_START_TIME, datetime.datetime.now())
            self.api.store_var(StoreKeys.CURRENTLY_WORKING, True)

            # Log clock-in info into employer's file
            self.clock_in(
                self.api.get_var(StoreKeys.EMPLOYER),
                self.api.get_var(
                    StoreKeys.WORK_START_TIME).strftime(
                        '%a %b %d, %Y %I:%M %p'
                )
            )

            self.bs.respond(
                'You\'ve been clocked in for {}.'
                .format(self.api.get_var(StoreKeys.EMPLOYER)))

        return

    def clock_in(self, employer, work_start_time):
        '''
        Writes line in employer specific file saying I have logged in to work.
        Arguments: <string> employer name,
                   <datetime.datetime object> work_start_time
        Return type: None
        '''
        # find/create employer file
        with open(
            os.path.join(self.work_study_dir,
                         '{}_hours.txt'.format(employer)), 'a+'
        ) as file:
            file.write('Started work: {}\n'.format(work_start_time))

    def get_employers(self):
        '''
        Gets a list of all employers from the employer database.
        '''
        employer_db_path = self.config["Database"]["employers"]
        employer_db = TinyDB(employer_db_path)
        return [item["name"] for item in employer_db.all()]
