'''
This feature sends an email to one of your contacts.
Be sure to put your gmail credential files into the gmail_credentials folder.
'''
from features.default import BaseFeature
import difflib
import ezgmail
import tempfile
import subprocess
import json
import re
from tinydb import TinyDB, Query
from features.feature_helpers import get_search_query


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "send_email"
        self.patterns = [
            "send an email",
            "send an email to"
        ]
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

        contacts_db_path = self.config['Database']['contacts']
        self.contacts_db = TinyDB(contacts_db_path)
        self.gmail_creds_folder = self.config['Folders']['gmail_credentials']

    def action(self, spoken_text, arguments_list: list = []):
        # Set the input queue of the speech object to the arguments list if it
        # exists. This will ensure that all hear & approve commands in this
        # feature will get input from the arguments list in order instead of
        # asking the user for input. Hence, the arguments list provided should
        # have as many items as there are hear & approve commands in this
        # feature.
        if (len(arguments_list) > 0):
            self.bs.set_input_queue(arguments_list)
        recipient = self.get_recipient(spoken_text)
        if not recipient:
            recipient = self.bs.ask_question(
                'Who do you want to send the email to?')
            if not recipient:
                return

        close_names = []
        known_contacts = self.get_contact_names()
        while close_names == []:
            close_names = difflib.get_close_matches(recipient, known_contacts)
            if close_names == []:
                recipient = self.bs.ask_question(
                    """Could not find this contact. Please try again
                    (say 'stop' or 'cancel' to exit."""
                )
                if not recipient:
                    return
        try:
            recipient_email = self.get_email(close_names[0])
        except Exception as e:
            print(e)
            self.bs.respond(
                """An error occured.
                 I will stop trying to send an email now."""
            )
            return

        # get subject
        subject = self.bs.ask_question('What is the subject of your email?')
        if not subject:
            return

        # get message
        message = self.bs.ask_question('What is the message of your email?')
        if not message:
            return

        # show summary email
        self.bs.respond('Here is a summary of your email:')
        print(self.summary_email(recipient_email, subject, message))

        # edit email
        if self.bs.approve("Would you like to edit this?"):
            edited_email = self.term_email_edit(
                recipient_email, subject, message)
            edited_email_json = json.loads(edited_email)
            recipient_email = edited_email_json["recipient_email"]
            subject = edited_email_json["subject"]
            message = edited_email_json["message"]
            self.bs.respond('Here is another summary of your email:')
            print(self.summary_email(recipient_email, subject, message))
        if self.bs.approve("Would you like to send this email?"):
            # send email
            ezgmail.init(
                tokenFile=self.gmail_creds_folder+'token.json',
                credentialsFile=self.gmail_creds_folder+'credentials.json'
            )
            message += "\n\n Bumblebee (Zintan's ai assistant)"
            ezgmail.send(recipient_email, subject, message)
            self.bs.respond('I have sent the email.')
        else:
            self.bs.respond('Okay.')
        return

    def summary_email(self, recipient_email, subject, message):
        '''
        Returns summary information of email details as heard from user.
        Arguments: <string> recipient, <string> subject, <string> message
        Return type: <string> summary
        '''
        summary = 'To: {}\nSubject: {}\nMessage: {}'.format(
            recipient_email, subject, message
        )
        return summary

    def term_email_edit(self, recipient_email, subject, message):
        '''
        Allows user to edit email details from within the nano text
        editor.
        '''
        f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        n = f.name
        f.writelines([recipient_email, '\n', subject, '\n', message])
        f.close()
        subprocess.call(['nano', n])
        with open(n, 'r') as f:
            recipient_email = f.readline()
            subject = f.readline()
            message = f.read()
        email_details = {}
        email_details["recipient_email"] = recipient_email
        email_details["subject"] = subject
        email_details["message"] = message
        email_details_json = json.dumps(email_details)
        return email_details_json

    def get_contact_names(self):
        '''Returns a list of names in contacts database'''
        names = []
        for item in self.contacts_db:
            names.append(item['name'])
        return names

    def get_email(self, name):
        '''Returns email of recipient given the name.'''
        Person = Query()
        results_list = self.contacts_db.search(
            Person.name.matches(name, flags=re.IGNORECASE)
        )
        email = results_list[0]['email']
        return email

    def get_recipient(self, spoken_text):
        '''Returns the recipient's name from spoken text.'''
        search_terms = ['to']
        recipient = get_search_query(
            spoken_text,
            self.patterns,
            search_terms
        )
        return recipient
