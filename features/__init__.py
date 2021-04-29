'''
Contains all the modules that should be available when this folder is imported.
'''
__all__ = [
    'google_search',
    'bumble_help',
    'clock_in',
    'clock_out',
    'greeting',
    'grepapp_search',
    'send_email',
    # 'open_notepad',
    'wiki_search',
    'wolfram_search',
    'start_research_server',
    'stop_research_server',
    'store_research_data',
    'silent_mode_on',
    'silent_mode_off',
    'youtube_search',
    'add_zoom_link',
    'open_zoom_link',
    'sleep',
    'stop_listening',
    'add_contact',
    'add_employer'
]

'''Essential Features that should be included in every custon list.'''
__essential__ = [
    'sleep',
    'stop_listening',
    'silent_mode_on',
    'silent_mode_off'
    ]

'''Features to test'''
__test__ = __essential__ + [
    'send_email',
    'open_zoom_link'
    ]

'''Contains cybersecurity specific features.'''
__cybersecurity__ = __essential__ + []

'''Contains geo specific features.'''
__geo__ = __essential__ + []
