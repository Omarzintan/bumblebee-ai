#!python3

from tkinter import *
import json

'''
Opens a Tkinter window to allow the user to edit the research topic as heard.
Argument: <string> topic
Return type: <JSON> topic_details_json
'''
def topic_edit(topic):
    root = Tk()
    root.geometry("320x100")
    root.title("Edit research topic")
    content = Frame(root)
    content.pack()
    topic_details = {}

    # creating topic field
    Label(content, text="Topic").grid(row=0, column=0, padx=5, sticky='sw')

    topic_entry = Entry(content, width=24)
    topic_entry.grid(row=0, column=1, padx=5)

    # inserting previous topic
    topic_entry.insert(END, topic)

    # retrieve edited topic from window
    def saveInput():
        topic_details["topic"] = str(topic_entry.get())
        root.destroy()

    def clear():
        topic_entry.delet(0, "end")

    # Buttons for saving and clearing
    saveButton = Button(content, text="Save", command=saveInput)
    clearButton = Button(content, text="Clear", command=clear)
    saveButton.grid(row=1, column=1, padx=5, sticky='e')
    clearButton.grid(row=1, column=1, padx=5, sticky='w')

    root.mainloop()

    topic_details_json = json.dumps(topic_details)
    return topic_details_json
