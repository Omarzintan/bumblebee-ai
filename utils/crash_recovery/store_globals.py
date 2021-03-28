from features.research import helpers as research_help
from features.research import glocal_vars as research_glocal
from core import Bumblebee
import json, pickle
import os, sys
import datetime

'''
 Names of gloabal variables desired to be stored in case of a crash
as seen in global_vars.py only for documentation purposes.
global_vars_needed = ['work_start_time','currently_working','employer']
'''

crash_file = 'crash_recovery.p'
global_vars_store = {}

# Store necessary global variables in global_vars.py
def store_vars():
    global_vars_store['work_start_time'] = Bumblebee.work_start_time
    global_vars_store['currently_working'] = Bumblebee.currently_working
    global_vars_store['employer'] = Bumblebee.employer
    with open(crash_file, 'wb') as f:
        f.seek(0)
        pickle.dump(global_vars_store, f)
    return
        
def restore_vars():
    global_vars_store = pickle.load(open(crash_file, "rb"))
    Bumblebee.work_start_time = global_vars_store['work_start_time']
    Bumblebee.currently_working = global_vars_store['currently_working']
    Bumblebee.employer = global_vars_store['employer']
    return
    
def start_gracefully():
    try:
        if os.path.exists(crash_file):
            print('Starting gracefully.')
            restore_vars()
            os.remove(crash_file)
    except:
        print(sys.exc_info())
        print('Start gracefully failed.')
        pass
    return

def exit_gracefully():
    print('Exiting gracefully.')
    if Bumblebee.research_server_proc:
        bs.respond('Closing research server gracefully.')
        research_help.store_data()
        research_help.stop_server()
    if global_vars.currently_working:
        store_vars()
