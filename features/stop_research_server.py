from features.default import BaseFeature
from core import Bumblebee
import os, sys

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = 'stop_research_server'
        self.patterns =  ["stop research", "exit research mode", "done researching"]
        super().__init__()

    def action(self, spoken_text=''):
        self.bs.respond('Stopping research server.')
        self.stop_server()
        return

    '''Stops the flask server for research mode.'''
    def stop_server(self):
        print(Bumblebee.research_server_proc)
        print(Bumblebee.research_server_proc.pid)
        try:
            Bumblebee.research_server_proc.kill()
            Bumblebee.research_server_proc = ''
            print('Server stopped')
        except:
            print("Unexpected error:", sys.exc_info())
            self.bs.respond('The server does not seem to be running')
