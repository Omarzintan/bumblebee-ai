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

# Find a way of handling crash files for multiple bees.


def store_internal_state(bee):
    '''Stores variables in a pickle file.'''
    with open(CRASH_FILE, 'wb') as f:
        f.seek(0)
        # TODO: Make get_internal_state an instance funciton.
        pickle.dump(bee.get_internal_state(), f)


def restore_internal_state(bee):
    '''Restores pickled variables.'''
    restored_state = pickle.load(open(CRASH_FILE, "rb"))
    # TODO: Make load_internal_state and instance function.
    bee.load_internal_state(restored_state)


def start_gracefully(bee):
    '''Restores stored global vars from before crash happened.'''
    try:
        if os.path.exists(CRASH_FILE):
            print('Starting gracefully.')
            restore_internal_state(bee)
            os.remove(CRASH_FILE)
    except OSError as exception:
        print(exception)
        print('Start gracefully failed.')


def exit_gracefully(bee, crash_happened=False):
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
        store_internal_state(bee)
        return

    # If this is a regular exiting, we ensure all threads are
    # terminated before we exit.
    for thread_failsafe in bee.thread_failsafes:
        bee.run_by_tags(thread_failsafe["termination_features"])

    bee.wake_word_detector.stop()
