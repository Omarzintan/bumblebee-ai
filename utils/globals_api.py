'''
Internal API for storing and retrieving global variables to be shared
between features.
'''
from core import Bumblebee


class GLOBALSAPI():
    '''
    Main API class
    '''

    CRASH_FILE = 'crash_recovery.p'

    def store(self, name: str, value):
        """
        Stores variable in Bumblebee global_store.
        Arguments: <string> name, value
        Returns: None
        """
        Bumblebee.global_store[name] = value

    def retrieve(self, name: str):
        """
        Retrieves a variable from Bumblebee global_store.
        Arguments: <string> name
        Returns if found: value of variable name stored in global_store
        Returns if not found: None
        """
        try:
            return Bumblebee.global_store[name]
        except KeyError:
            print(f"could not retrieve {name} from global_store.")
            return None

    def add_thread_failsafe(self, proc_id: int,
                            terminate=["terminate_all_threads"]):
        """
        Inserts a record of a running thread into the threads
        list in Bumblebee.
        Arguments: <int> proc_id (process id of the thread),
                   <list> terminate (list of commands to run in
                                     order to terminate thread)
        Returns: None
        """
        thread_failsafe = {}
        thread_failsafe["proc_id"] = proc_id
        thread_failsafe["terminate"] = terminate

        Bumblebee.global_store['threads'].append(thread_failsafe)

    def remove_thread_failsafe(self, proc_id: int):
        """
        Removes record of running thread from threads list
        in Bumblebee.
        Arguments: <int> proc_id (process id of the thread)
        Returns: None
        """
        try:
            threads = Bumblebee.global_store['threads']
            result = [
                thread for thread in threads if not (
                    thread['proc_id'] == proc_id
                )
            ]
            Bumblebee.global_store['threads'] = result
                    

        except KeyError:
            print(f"No thread with id {proc_id} found.")
