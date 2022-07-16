'''Feature to start research server.'''
import json
import threading
import tempfile
import subprocess
from features.default import BaseFeature


class StoreKeys:
    RESEARCH_TOPIC = 'research_topic'
    RESEARCH_SERVER_PROC_ID = 'research_server_proc_id'


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "start_research_server"
        self.patterns = [
            "start research",
            "research mode",
            "let's do research",
            "start research server"
        ]
        self.api = bumblebee_api
        self.config = self.api.get_config()
        self.bs = self.api.get_speech()

    def action(self, spoken_text, arguments_list: list = []):
        topic = self.bs.ask_question('What is the topic of your research?')
        if not topic:
            return
        self.bs.respond('Starting research mode on {}'.format(topic))
        if self.bs.approve("Would you like to edit this?"):
            edited_topic = self.term_topic_edit(topic)
            edited_json = json.loads(edited_topic)
            topic = edited_json["topic"]
        self.bs.respond('Starting server for research on {}'.format(topic))
        self.api.store_var(StoreKeys.RESEARCH_TOPIC, topic)
        # start python flask server in new thread
        threading.Thread(target=self.start_server).start()

    def term_topic_edit(self, topic):
        '''
        Allows user to edit the research topic from within the nano text
        editor.
        '''
        f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        n = f.name
        f.writelines([topic])
        f.close()
        subprocess.call(['nano', n])
        with open(n, 'r') as f:
            topic = f.readline()
        topic_details = {}
        topic_details["topic"] = topic
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
        self.api.store_var(
            StoreKeys.RESEARCH_SERVER_PROC_ID,
            research_server_proc.pid
        )
        self.api.add_thread_failsafe(
            research_server_proc.pid,
            ["store_research_data", "stop_research_server"]
        )
