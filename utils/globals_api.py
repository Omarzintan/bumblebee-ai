from core import Bumblebee

crash_file = 'crash_recovery.p'

"""
Stores variable in Bumblebee global_store.
Arguments: <string> name, value
Returns: None
"""
def store(name:str, value):
    Bumblebee.global_store[name] = value
    return

"""
Retrieves a variable from Bumblebee global_store.
Arguments: <string> name
Returns if found: value of variable name stored in global_store
Returns if not found: None
"""
def retrieve(name:str):
    try:
        return Bumblebee.global_store[name]
    except:
        print(f"could not retrieve {name} from global_store.")
        return None

"""
FUNCTIONS NECESSARY FOR CRASH RECOVERY
Crash recovery entails storing desired global variables in case
a crash happens. So far, the employee info is stored and preserved 
if the user is currently working. On reboot, the information about 
much time has been spent working is restored. Also, if the research
server process is running, it is killed before reboot happens.
"""
"""Stores variables in a pickle file."""
def store_vars():
    with open(crash_file, 'wb') as f:
        f.seek(0)
        pickle.dump(Bumblebee.global_store, f)
    return

"""Restores pickled variables."""
def restore_vars():
    Bumblebee.global_store = pickle.load(open(crash_file, "rb"))
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

# FIX THIS
def exit_gracefully():
    print('Exiting gracefully.')
    if retrieve("research_server_proc") != "":
        Bumblebee.speech.respond('Closing research server gracefully.')
        store_research_feature_index = .feature_indices['store_research_data']
        stop_research_feature_index = .feature_indices['stop_research_data']
        ._features[store_research_feature_index].action()
        _features[stop_research_feature_index].action()
    if Bumblebee.currently_working:
        store_vars()    
