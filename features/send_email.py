from features.default import BaseFeature
import difflib
import ezgmail
import json
import re
import PySimpleGUI as sg
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
        self.bumblebee_dir = self.config['Common']['bumblebee_dir']

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
            self.bs.respond('Who do you want to send the email to?')
            recipient = self.bs.hear()
            if self.bs.interrupt_check(recipient):
                return

        close_names = []
        known_contacts = self.get_contact_names()
        while close_names == []:
            close_names = difflib.get_close_matches(recipient, known_contacts)
            if close_names == []:
                self.bs.respond(
                    """Could not find this contact. Please try again
                    (say 'stop' or 'cancel' to exit."""
                )
                recipient = self.bs.hear()
                if self.bs.interrupt_check(recipient):
                    break
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
        self.bs.respond('What is the subject of your email?')
        subject = self.bs.hear()
        if self.bs.interrupt_check(subject):
            return

        # get message
        self.bs.respond('What is the message of your email?')
        message = self.bs.hear()
        if self.bs.interrupt_check(message):
            return

        # show summary email
        self.bs.respond('Here is a summary of your email:')
        print(self.summary_email(recipient_email, subject, message))

        # edit email
        if self.bs.approve("Would you like to edit this?"):
            edited_email = self.email_edit(recipient_email, subject, message)
            edited_email_json = json.loads(edited_email)
            recipient_email = edited_email_json["recipient_email"]
            subject = edited_email_json["subject"]
            message = edited_email_json["message"]
            self.bs.respond('Here is another summary of your email:')
            print(self.summary_email(recipient_email, subject, message))
        if self.bs.approve("Would you like to send this email?"):
            # send email
            ezgmail.init(
                tokenFile=self.bumblebee_dir+'token.json',
                credentialsFile=self.bumblebee_dir+'credentials.json'
            )
            message += "\n\n\n Bumblebee (Zintan's ai assistant)"
            ezgmail.send(recipient_email, subject, message)
            self.bs.respond('I have sent the email.')
        else:
            self.bs.respond('Okay.')
        return

    '''
    Returns summary information of email details as heard from user.
    Arguments: <string> recipient, <string> subject, <string> message
    Return type: <string> summary
    '''

    def summary_email(self, recipient_email, subject, message):
        summary = 'To: {}\nSubject: {}\nMessage: {}'.format(
            recipient_email, subject, message
        )
        return summary

    def email_edit(self, recipient_email, subject, message):
        '''
        Opens up a PySimpleGUI window with email details to allow the user to
        edit any of these details.
        Arguments: <string> recipient_email, <string> subject, <string> message
        Return type: <JSON> email_details_json
        '''
        sg.theme('DarkAmber')
        layout = [[sg.Text("To:"),
                   sg.InputText(default_text=recipient_email,
                                key="recipient_email")],
                  [sg.Text("Subject:"),
                   sg.InputText(default_text=subject, key="subject")],
                  [sg.Text("Message:"),
                   sg.InputText(default_text=message, size=(50, 10),
                                key="message")],
                  [sg.Submit(), sg.Cancel()]
                  ]
        event, values = sg.Window(
            "Edit Email", layout).read(close=True)
        email_details = {}
        email_details["recipient_email"] = str(values['recipient_email'])
        email_details["subject"] = str(values["subject"])
        email_details["message"] = str(values["message"])
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
