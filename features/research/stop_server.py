from features.default import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars, helpers
import os, sys
import signal

class Feature(BaseFeature):
    def __init__(self, keywords):
        self.tag_name = 'stop_research_server'
        self.patterns =  ["stop research", "exit research mode", "done researching"]
        self.index

    def action(self, spoken_text):
        bs.respond('Stopping research server.')
        self.stop_server()
        return

    '''Stops the flask server for research mode.'''
    def stop_server(self):
        print(glocal_vars.server_proc)
        print(glocal_vars.server_proc.pid)
        try:
            glocal_vars.server_proc.kill()
            glocal_vars.server_proc = ''
            print('Server stopped')
        except:
            print("Unexpected error:", sys.exc_info())
            bs.respond('The server does not seem to be running')
