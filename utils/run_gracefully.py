"""
Contains functions necessary for graceful running of Bumblebee.
This entails storing global variables in case of a crash and restoring them
on reboot.
This also includes stopping all running subprocesses before exiting Bumblebee.
"""
import os
import pickle
from core import Bumblebee
from utils import wake_word_detector
from utils.globals_api import GLOBALSAPI


CRASH_FILE = 'crash_recovery.p'
globals_api = GLOBALSAPI()


def store_vars():
    '''Stores variables in a pickle file.'''
    with open(CRASH_FILE, 'wb') as f:
        f.seek(0)
        pickle.dump(Bumblebee.global_store, f)


def restore_vars():
    '''Restores pickled variables.'''
    Bumblebee.global_store = pickle.load(open(CRASH_FILE, "rb"))


def start_gracefully():
    '''Restores stored global vars from before crash happened.'''
    try:
        if os.path.exists(CRASH_FILE):
            print('Starting gracefully.')
            restore_vars()
            os.remove(CRASH_FILE)
    except OSError as exception:
        print(exception)
        print('Start gracefully failed.')


def exit_gracefully(bumblebee, crash_happened=False):
    '''
    Exiting gracefully means checking for any running threads
    and terminating them as well as storing global variables if
    a crash happend.
    Arguments: <Bumblebee> bumblebee (an instance of Bumblebee),
               <boolean> crash_happened
    Returns: None
    '''
    print('Exiting gracefully.')
    # If a crash happened we store all global vars
    # includeing the proccess ids for all running
    # threads.
    if crash_happened:
        store_vars()
        return

    # If this is a regular exiting, we ensure all threads are
    # terminated before we exit.
    for thread_failsafe in Bumblebee.thread_failsafes:
        bumblebee.run_by_tags(thread_failsafe["termination_features"])

    wake_word_detector.stop()
