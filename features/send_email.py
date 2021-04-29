from features.default import BaseFeature
import difflib
import ezgmail
import json
import os
import re
from tkinter import *
import json
from tinydb import TinyDB, Query
from features.feature_helpers import get_search_query


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "send_email"
        self.patterns = [
            "send an email",
            "send an email to"
            ]
        super().__init__()

        contacts_db_path = self.config['Database']['contacts']
        self.contacts_db = TinyDB(contacts_db_path)
        self.bumblebee_dir = self.config['Common']['bumblebee_dir']

    def action(self, spoken_text):
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
                    'Could not find this contact. Please try again'
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
        self.bs.respond('Would you like to edit this?')
        edit = self.bs.hear()
        if self.bs.interrupt_check(edit):
            return
        if 'yes' in edit or 'yeah' in edit or 'sure' in edit:
            edited_email = self.email_edit(recipient_email, subject, message)
            edited_email_json = json.loads(edited_email)
            recipient_email = edited_email_json["recipient_email"]
            subject = edited_email_json["subject"]
            message = edited_email_json["message"]
            self.bs.respond('Here is another summary of your email:')
            print(self.summary_email(recipient_email, subject, message))
        self.bs.respond('Would you like to send this email?')
        approve = self.bs.hear()
        if self.bs.interrupt_check(approve):
            return
        if approve == 'yes' or approve == 'sure' or approve == 'yeah':
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

    '''
    Opens up a Tkinter window with email details to allow the user to edit
    any of these details.
    Arguments: <string> recipient_email, <string> subject, <string> message
    Return type: <JSON> email_details_json
    '''
    def email_edit(self, recipient_email, subject, message):
        root = Tk()
        root.geometry("300x300")
        root.minsize(height=350, width=500)
        root.maxsize(height=560, width=560)
        root.title("Edit Email")
        content = Frame(root)
        content.pack()
        email_details = {}

        # creating fields
        Label(content, text="To:").grid(row=0, column=0, padx=5, sticky='sw')
        Label(content, text="Subject:").grid(
            row=0, column=1, padx=5, sticky='sw'
            )
        Label(content, text="Message:").grid(
            row=2, column=0, padx=5, sticky='sw'
            )

        recip = Entry(content, width=24)
        subj = Entry(content, width=24)
        msg = Text(content, width=50, height=10)

        recip.grid(row=1, column=0, padx=5)
        subj.grid(row=1, column=1, padx=5)
        msg.grid(row=3, column=0, columnspan=2, padx=5)

        # inserting email info
        recip.insert(END, recipient_email)
        subj.insert(END, subject)
        msg.insert(END, message)

        # retrieve email details from edit fields and close windown
        def saveInput():
            email_details["recipient_email"] = str(recip.get())
            email_details["subject"] = subj.get()
            email_details["message"] = msg.get(1.0, "end-1c")
            root.destroy()

        def clear():
            recip.delete(0, "end")
            subj.delete(0, "end")
            msg.delete(1.0, "end")

        # Buttons for saving and clearing
        saveButton = Button(content, text="Save", command=saveInput)
        clearButton = Button(content, text="Clear", command=clear)
        saveButton.grid(row=4, column=0, padx=5, sticky='e')
        clearButton.grid(row=4, column=1, padx=5, sticky='w')

        root.mainloop()

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
