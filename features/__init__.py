'''
Contains all the modules that should be available when this folder is imported.
'''


__all__ = [
    'google_search',
    'bumble_help',
    'clock_in',
    'clock_out',
    'chatbot',
    'grepapp_search',
    'send_email',
    'open_notepad',
    'wiki_search',
    'wolfram_search',
    'start_research_server',
    'stop_research_server',
    'store_research_data',
    'silent_mode_on',
    'voice_mode_on',
    'youtube_search',
    'add_zoom_link',
    'open_zoom_link',
    'sleep',
    'stop_listening',
    'add_contact',
    'add_employer',
    'set_default_speech_mode',
    'load_routines',
    'run_routine'
]

'''Essential Features that should be included in every custon list.'''
__essential__ = [
    'sleep',
    'stop_listening',
    'silent_mode_on',
    'voice_mode_on',
    'set_default_speech_mode'
]

'''Contains cybersecurity specific features.'''
__cybersecurity__ = __essential__ + []

'''Contains geo specific features.'''
__geo__ = __essential__ + []


def create_feature_lists():
    feature_lists = {}
    feature_lists['all'] = __all__
    feature_lists['cybersecurity'] = __cybersecurity__
    feature_lists['geo'] = __geo__
    return feature_lists


feature_lists = create_feature_lists()
