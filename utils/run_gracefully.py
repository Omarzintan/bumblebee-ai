"""
Contains functions necessary for graceful running of Bumblebee.
This entails storing global variables in case of a crash and restoring them
on reboot.
This also includes stopping all running subprocesses before exiting Bumblebee.
"""
import os
import pickle


class GracefulRunner():
    def __init__(self, bee_instance):
        self.CRASH_FILE = 'crash_recovery.p'
        self.bee_instance = bee_instance

    # Find a way of handling crash files for multiple bees.

    def store_internal_state(self):
        '''Stores variables in a pickle file.'''
        with open(self.CRASH_FILE, 'wb') as f:
            f.seek(0)
            pickle.dump(self.bee_instance.get_internal_state(), f)

    def restore_internal_state(self):
        '''Restores pickled variables.'''
        restored_state = pickle.load(open(self.CRASH_FILE, "rb"))
        self.bee_instance.load_internal_state(restored_state)

    def start_gracefully(self):
        '''Restores stored global vars from before crash happened.'''
        try:
            if os.path.exists(self.CRASH_FILE):
                print('Starting gracefully.')
                self.restore_internal_state()
                os.remove(self.CRASH_FILE)
        except OSError as exception:
            print(exception)
            print('Start gracefully failed.')

    def exit_gracefully(self, crash_happened=False):
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
            self.store_internal_state()
            return

        # If this is a regular exiting, we ensure all threads are
        # terminated before we exit.
        for thread_failsafe in self.bee_instance.thread_failsafes:
            self.bee_instance.run_by_tags(
                thread_failsafe["termination_features"])

        self.bee_instance.wake_word_detector.stop()
