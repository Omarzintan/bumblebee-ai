from features.default import BaseFeature
from features.contacts import helpers as contact_help
import difflib
import ezgmail
import json
import os
from tkinter import *
import json


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "send_email"
        self.patterns = ["send an email", "send an email to"]
        self.index

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
        print(self.summary_email(recipient, subject, message))

        # edit email
        bs.respond('Would you like to edit this?')
        edit = ''
        edit = bs.infinite_speaking_chances(edit)
        if bs.interrupt_check(edit):
            return
        if 'yes' in edit or 'yeah' in edit:
            edited_email = self.email_edit(recipient, subject, message)
            edited_email_json = json.loads(edited_email)
            recipient = edited_email_json["recipient"]
            subject = edited_email_json["subject"]
            message = edited_email_json["message"]
            bs.respond('Here is another summary of your email:')
            print(self.summary_email(recipient, subject, message))
        bs.respond('Would you like to send this email?')
        approve = ''
        approve = bs.infinite_speaking_chances(approve)
        if bs.interrupt_check(approve):
            return
        if approve == 'yes':
            # send email
            ezgmail.init(tokenFile=os.getenv('BUMBLEBEE_PATH')+'token.json', credentialsFile=os.getenv('BUMBLEBEE_PATH')+'credentials.json')
            message += "\n\n\n Bumblebee (Zintan's ai assistant)"
            ezgmail.send(recipient, subject, message)
            bs.respond('I have sent the email.')
        else:
            bs.respond('Okay.')
        return


    '''
    Returns summary information of email details as heard from user.
    Arguments: <string> recipient, <string> subject, <string> message
    Return type: <string> summary
    '''
    def summary_email(self, recipient, subject, message):
        summary = 'To: {}\nSubject: {}\nMessage: {}'.format(recipient, subject, message)
        return summary

    '''
    Opens up a Tkinter window with email details to allow the user to edit any of these details.
    Arguments: <string> recipient, <string> subject, <string> message
    Return type: <JSON> email_details_json
    '''
    def email_edit(self, recipient, subject, message):
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
        Label(content, text="Subject:").grid(row=0, column=1, padx=5, sticky='sw')
        Label(content, text="Message:").grid(row=2, column=0, padx=5, sticky='sw')

        recip = Entry(content, width=24)
        subj = Entry(content, width=24)
        msg = Text(content, width=50, height=10)
    
        recip.grid(row=1, column=0, padx=5)
        subj.grid(row=1, column=1, padx=5)
        msg.grid(row=3, column=0, columnspan=2, padx=5)

        # inserting email info
        recip.insert(END, recipient)
        subj.insert(END, subject)
        msg.insert(END, message)
    
        # retrieve email details from edit fields and close windown
        def saveInput():
            email_details["recipient"] = str(recip.get())
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
