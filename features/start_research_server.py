#from features.features import BaseFeature
from features.default import BaseFeature
import json
import threading
import subprocess, signal
import logging, selectors
import sys
import os
import datetime

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "start_research_server"
        self.patterns = ["start research", "research mode" "let's do research", "start research server"]
        self.index
        
    def action(self, spoken_text):
        bs.respond('What is the topic of your research?')
        topic = ''
        topic = bs.infinite_speaking_chances(topic)
        if bs.interrupt_check(topic):
            return
        bs.respond('Starting research mode on {}'.format(topic))
        bs.respond('Would you like to edit this?')
        edit = ''
        edit = bs.infinite_speaking_chances(edit)
        if bs.interrupt_check(edit):
            return
        if 'yes' in edit or 'yeah' in edit:
            edited_topic = self.topic_edit(topic)
            edited_json = json.loads(edited_topic)
            topic = edited_json["topic"]
        bs.respond('Starting server for research on {}'.format(topic))
        glocal_vars.research_topic = topic
        # start python flask server in new thread
        threading.Thread(target=self.start_server).start()

    '''
    Opens a Tkinter window to allow the user to edit the research topic as heard.
    Argument: <string> topic
    Return type: <JSON> topic_details_json
    '''
    def topic_edit(self, topic):
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
        
    '''Starts the flask server for research mode.'''
    def start_server(self):
        # Create the subprocess for the flask server.
        glocal_vars.server_proc = subprocess.Popen([os.environ.get('PYTHON3_ENV'), bumblebee_root+'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid())
        return
