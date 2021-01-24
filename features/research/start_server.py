from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars, helpers
import json
import threading
import subprocess, signal
import logging, selectors
import sys
import os
import datetime

class StartServer(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords
        
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
            edited_topic = helpers.topic_edit(topic)
            edited_json = json.loads(edited_topic)
            topic = edited_json["topic"]
        bs.respond('Starting server for research on {}'.format(topic))
        glocal_vars.research_topic = topic
        # start python flask server in new thread
        threading.Thread(target=self.start_server).start()


    '''Starts the flask server for research mode.'''
    def start_server(self):
        logging.basicConfig(filename=os.environ.get('BUMBLEBEE_PATH')+'server.log', level=logging.INFO)

        # log the date and time in log file
        logging.info(datetime.datetime.now().strftime('%d:%m:%Y, %H:%M:%S'))
        # Create the subprocess for the flask server.
        glocal_vars.server_proc = subprocess.Popen([os.environ.get('PYTHON3_ENV'), os.environ.get('BUMBLEBEE_PATH')+'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
                   
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

