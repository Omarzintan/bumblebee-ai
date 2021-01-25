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
        threading.Thread(target=helpers.start_server).start()
