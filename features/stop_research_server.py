import os
import signal
from features.default import BaseFeature
from features.start_research_server import StoreKeys as research_store


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = 'stop_research_server'
        self.patterns = [
            "stop research",
            "exit research mode",
            "done researching"
        ]
        self.api = bumblebee_api
        self.bs = self.api.get_speech()

    def action(self, spoken_text: str = "", arguments_list: list = []):
        self.bs.respond('Stopping research server.')
        self.stop_server()
        return

    def stop_server(self):
        '''Stops the flask server for research mode.'''
        server_proc_id = self.api.pop_var(
            research_store.RESEARCH_SERVER_PROC_ID
        )
        print(server_proc_id)
        try:
            os.kill(server_proc_id, signal.SIGTERM)
            self.api.remove_thread_failsafe(server_proc_id)
            print('Server stopped')
        except OSError as exception:
            print("Unexpected error:", exception)
            self.bs.respond('The server does not seem to be running')
