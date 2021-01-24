from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars
import os, sys
import signal

class StopServer(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond('Stopping research server.')
        self.stop_server()
        return

    def stop_server(self):
        print(glocal_vars.server_proc)
        print(glocal_vars.server_proc.pid)
        try:
            os.killpg(os.getpgid(glocal_vars.server_proc.pid), signal.SIGTERM)
            print('Server stopped')
        except:
            print("Unexpected error:", sys.exc_info())
            bs.respond('The server does not seem to be running')
            
