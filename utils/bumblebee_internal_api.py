'''
Internal API Bumblebee. Functions include:
    Handling global variables that need to be shared
between features.
    Modifying characteristics of the bee instance running
the features.
    Exposes certain function of the bee instance to features.
    Utility functions for tracking and safely removing threaded
feature actions.
'''


class BUMBLEBEEAPI():

    def __init__(self, bee_instance):
        self.bee_instance = bee_instance

    def store_var(self, name: str, value):
        """
        Stores variable in Bee global_store.
        Arguments: <string> name, value
        Returns: None
        """
        self.bee_instance.global_store[name] = value

    def get_var(self, name: str):
        """
        Retrieves a variable from Bee global_store.
        Arguments: <string> name
        Returns if found: value of variable name stored in global_store
        Returns if not found: None
        """
        try:
            return self.bee_instance.global_store[name]
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

        self.bee_instance.thread_failsafes.append(thread_failsafe)

    def remove_thread_failsafe(self, proc_id: int):
        """
        Removes record of running thread from threads list
        in Bee.
        Arguments: <int> proc_id (process id of the thread)
        Returns: None
        """
        try:
            result = []
            for thread_failsafe in self.bee_instance.thread_failsafes:
                if not thread_failsafe['proc_id'] == proc_id:
                    result.append(thread_failsafe)

            self.bee_instance.thread_failsafes = result

        except KeyError:
            print(f"No thread failsafe with id {proc_id} was found.")

    def get_config(self):
        """
        Get the config file for the bee instance.
        """
        return self.bee_instance.get_config()

    def get_speech(self):
        """
        Get the BumbleSpeech instance of the bee instance.
        """
        return self.bee_instance.get_speech()

    def run_by_tags(self, feature_tags: list):
        """
        Run a list of feature actions given their tags.
        """
        self.bee_instance.run_by_tags(feature_tags)

    def sleep_on(self):
        self.bee_instance.sleep = 1
