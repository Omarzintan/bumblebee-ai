#!python3
from features import wake_word_detector
from features.global_vars import bumble_speech as bs
from features.keywords import Keywords
from features import configs
from features import global_vars

def run():
    bs.respond('Hey.')
    while(global_vars.sleep == 0):
        action_found = False
        bs.respond('How may I help you?')
        text = ''
        text = bs.infinite_speaking_chances(text)

        for config in configs.config_actions:
            if any(word in text for word in config.keywords):
                action_found = True
                config.action(text)
                break
        if not action_found:
            bs.respond('I do not know how to do this yet.')
        
        
if __name__ == '__main__':    
    while(1):
        if wake_word_detector.run():
            global_vars.sleep = 0
            run()
