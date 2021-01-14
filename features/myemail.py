#!python3

from tkinter import *
import json

'''
Returns summary information of email details as heard from user.
Arguments: <string> recipient, <string> subject, <string> message
Return type: <string> summary
'''
def summary_email(recipient, subject, message):
    summary = 'To: {}\nSubject: {}\nMessage: {}'.format(recipient, subject, message)
    return summary

'''
Opens up a Tkinter window with email details to allow the user to edit any of these details.
Arguments: <string> recipient, <string> subject, <string> message
Return type: <JSON> email_details_json
'''
def email_edit(recipient, subject, message):
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
