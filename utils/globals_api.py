'''
Internal API for storing and retrieving global variables to be shared
between features.
'''
from core import Bee


class GLOBALSAPI():
    '''
    Main API class
    '''

    CRASH_FILE = 'crash_recovery.p'

    def store(self, name: str, value):
        """
        Stores variable in Bee global_store.
        Arguments: <string> name, value
        Returns: None
        """
        Bee.global_store[name] = value

    def retrieve(self, name: str):
        """
        Retrieves a variable from Bee global_store.
        Arguments: <string> name
        Returns if found: value of variable name stored in global_store
        Returns if not found: None
        """
        try:
            return Bee.global_store[name]
        except KeyError:
            print(f"could not retrieve {name} from global_store.")
            return None

    def add_thread_failsafe(self, proc_id: int,
                            termination_features=[]):
        """
        Inserts a record of a running thread into the threads
        list in Bee.
        Arguments: <int> proc_id (process id of the thread),
                   <list> termination_features (list of feature tags,
                    indicating features to run in order to terminate thread.
                    These features are run when exiting gracefully)
        Returns: None
        """
        thread_failsafe = {}
        thread_failsafe["proc_id"] = proc_id
        thread_failsafe["termination_features"] = termination_features

        Bee.thread_failsafes.append(thread_failsafe)

    def remove_thread_failsafe(self, proc_id: int):
        """
        Removes record of running thread from threads list
        in Bee.
        Arguments: <int> proc_id (process id of the thread)
        Returns: None
        """
        try:
            result = [
                thread_failsafe for thread_failsafe in Bee.thread_failsafes if not (
                    thread_failsafe['proc_id'] == proc_id
                )
            ]

            Bee.thread_failsafes = result

        except KeyError:
            print(f"No thread failsafe with id {proc_id} was found.")
