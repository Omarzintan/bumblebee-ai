#!python3
from features import wake_word_detector
from features.global_vars import bumble_speech as bs
from features.keywords import Keywords
from features import configs
from features import global_vars
from features.crash_recovery import store_globals as cr

def run():
    bs.respond('Hey.')
    bs.respond('How may I help you?')

    while(global_vars.sleep == 0):
        action_found = False
        text = ''
        text = bs.infinite_speaking_chances(text)

        for config in configs.config_actions:
            if any(word in text.lower() for word in config.keywords):
                action_found = True
                config.action(text)
                break
        if not action_found:
            # for generic conversations
            configs.wolfram_search.action(text)
        
if __name__ == '__main__':    
    while(1):
        try:
            cr.start_gracefully()
            if wake_word_detector.run():
                global_vars.sleep = 0
                run()
        except IOError:
            cr.exit_gracefully()
