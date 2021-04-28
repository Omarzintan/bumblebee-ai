'''Feature to start research server.'''
import json
import threading
import subprocess
from features.default import BaseFeature
from core import Bumblebee
from tkinter import *


class StoreKeys:
    RESEARCH_TOPIC = 'research_topic'
    RESEARCH_SERVER_PROC_ID = 'research_server_proc_id'


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "start_research_server"
        self.patterns = [
            "start research",
            "research mode",
            "let's do research",
            "start research server"
            ]
        super().__init__()

    def action(self, spoken_text):
        self.bs.respond('What is the topic of your research?')
        topic = self.bs.hear()
        if self.bs.interrupt_check(topic):
            return
        self.bs.respond('Starting research mode on {}'.format(topic))
        self.bs.respond('Would you like to edit this?')
        edit = self.bs.hear()
        if self.bs.interrupt_check(edit):
            return
        if 'yes' in edit or 'yeah' in edit:
            edited_topic = self.topic_edit(topic)
            edited_json = json.loads(edited_topic)
            topic = edited_json["topic"]
        self.bs.respond('Starting server for research on {}'.format(topic))
        self.globals_api.store(RESEARCH_TOPIC, topic)
        # start python flask server in new thread
        threading.Thread(target=self.start_server).start()

    def topic_edit(self, topic):
        '''
        Opens a Tkinter window to allow the user to edit the research
        topic as heard.
        Argument: <string> topic
        Return type: <JSON> topic_details_json
        '''
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

    def start_server(self):
        '''Starts the flask server for research mode.'''
        python3_path = self.config['Common']['python3_path']
        bumblebee_dir = self.config['Common']['bumblebee_dir']
        # Create the subprocess for the flask server.
        research_server_proc = subprocess.Popen(
            [python3_path, bumblebee_dir+'server.py'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.globals_api.store(
            RESEARCH_SERVER_PROC_ID,
            research_server_proc.pid
        )
        self.globals_api.add_thread_failsafe(
            research_server_proc.pid,
            ["store_research_data", "stop_research_server"]
        )
