from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.myemail import helpers
from features.contacts import helpers as contact_help
import difflib
import ezgmail
import json

class SendEmail(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond('Who do you want to send the email to?')
        name = ''
        name = bs.infinite_speaking_chances(name)
        if bs.interrupt_check(name):                
            return
        close_names = []
        while close_names == []:
            close_names = difflib.get_close_matches(name, contact_help.get_names())
            if close_names == []:
                bs.respond('Could not find this contact. Please try again')
                name = ''
                name = bs.infinite_speaking_chances(name)
                if bs.interrupt_check(name):
                    break
        try:
            recipient = contact_help.get_email(close_names[0])
            print(recipient)
        except:
            bs.respond("I will cease trying to send an email now.")
            return
        # get subject
        bs.respond('What is the subject of your email?')
        subject = ''
        subject = bs.infinite_speaking_chances(subject)
        if bs.interrupt_check(subject):
            return
        # get message
        bs.respond('What is the message of your email?')
        message = ''
        message = bs.infinite_speaking_chances(message)
        if bs.interrupt_check(message):
            return
        # show email
        bs.respond('Here is a summary of your email:')
        print(helpers.summary_email(recipient, subject, message))

        # edit email
        bs.respond('Would you like to edit this?')
        edit = ''
        edit = bs.infinite_speaking_chances(edit)
        if bs.interrupt_check(edit):
            return
        if 'yes' in edit or 'yeah' in edit:
            edited_email = helpers.email_edit(recipient, subject, message)
            edited_email_json = json.loads(edited_email)
            recipient = edited_email_json["recipient"]
            subject = edited_email_json["subject"]
            message = edited_email_json["message"]
            bs.respond('Here is another summary of your email:')
            print(helpers.summary_email(recipient, subject, message))
        bs.respond('Would you like to send this email?')
        approve = ''
        approve = bs.infinite_speaking_chances(approve)
        if bs.interrupt_check(approve):
            return
        if approve == 'yes':
            # send email
            ezgmail.init()
            message += "\n\n\n Bumblebee (Zintan's ai assistant)"
            ezgmail.send(recipient, subject, message)
            bs.respond('I have sent the email.')
        else:
            bs.respond('Okay.')
