'''Helper Functions for research features.'''

from tkinter import *
import json
import os, sys
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars
import subprocess
import signal
import logging, selectors
import datetime
from helpers import bumblebee_root

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

'''Stops the flask server for research mode.'''
def stop_server():
    print(glocal_vars.server_proc)
    print(glocal_vars.server_proc.pid)
    try:
        os.killpg(os.getpgid(glocal_vars.server_proc.pid), signal.SIGTERM)
        glocal_vars.server_proc = ''
        print('Server stopped')
        return
    except:
        print("Unexpected error:", sys.exc_info())
        bs.respond('The server does not seem to be running')
        return

    
'''Starts the flask server for research mode.'''
def start_server():
        logging.basicConfig(filename=bumblebee_root+'server.log', level=logging.INFO)

        # log the date and time in log file
        logging.info(datetime.datetime.now().strftime('%d:%m:%Y, %H:%M:%S'))
        # Create the subprocess for the flask server.
        glocal_vars.server_proc = subprocess.Popen([os.environ.get('PYTHON3_ENV'), bumblebee_root+'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
                   
        # Logging stdout and stderr from flask server in a way that preserves order.
        sel = selectors.DefaultSelector()
        sel.register(glocal_vars.server_proc.stdout, selectors.EVENT_READ)
        sel.register(glocal_vars.server_proc.stderr, selectors.EVENT_READ)

        while True:
            for key, _ in sel.select():
                data = key.fileobj.read1().decode()
                if not data:
                    exit()
                if key.fileobj is glocal_vars.server_proc.stdout:
                    # Send stdout to log file
                    logging.info(data)                
                else:
                    # Send stderr to log file
                    logging.info(data)
