"""
FUNCTIONS NECESSARY FOR CRASH RECOVERY
Crash recovery entails storing desired global variables in case
a crash happens. So far, the employee info is stored and preserved
if the user is currently working. On reboot, the information about
much time has been spent working is restored. Also, if the research
server process is running, it is killed before reboot happens.
"""


def store_vars():
    '''Stores variables in a pickle file.'''
    with open(crash_file, 'wb') as f:
        f.seek(0)
        pickle.dump(Bumblebee.global_store, f)
    return


def restore_vars():
    '''Restores pickled variables.'''
    Bumblebee.global_store = pickle.load(open(crash_file, "rb"))
    return


def start_gracefully():
    '''Restores stored global vars from before crash happened.'''
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
# check for any running processes and end them?
# 
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

