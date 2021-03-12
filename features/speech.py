'''Functions responsible for Bumblebee's speech recognition and responding'''

import speech_recognition as sr
import os, sys
import playsound
import pyttsx3
from helpers import bumblebee_root
import pdb

silent_mode = False
class BumbleSpeech():
    '''Function to set silent mode.'''
    def set_silent_mode(self, bool_val):
        global silent_mode
        if not isinstance(bool_val, (bool)):
            return -1
        silent_mode = bool_val
        return 0
    
    ''' Function to capture requests/questions.'''
    def hear(self):
        if silent_mode:
            #pdb.set_trace()
            input_data = input('type your response here: ')
            return input_data

            
        input_speech = sr.Recognizer()
        sr.energy_threshold = 4000 # makes adjusting to ambient noise more fine-tuned
        with sr.Microphone() as source:
            playsound.playsound(bumblebee_root+'sounds/tone-beep.wav', True)
            input_speech.adjust_for_ambient_noise(source)
            audio = input_speech.listen(source)
            input_data = ''
            try:
                input_data = input_speech.recognize_google(audio)
                print('You said, ' + input_data)
            except sr.UnknownValueError:
                self.respond('Sorry I did not hear you, please repeat.')
            except sr.RequestError:
                # This happens when there is not internet connection.
                self.respond('No internet connection found.')
                self.respond('Starting silent mode.')
                self.set_silent_mode(True)
        return input_data

    ''' Respond to requests/questions.'''
    def respond(self, output):
        if silent_mode:
            print(output)
            return

        num = 0
        print(output)
        num += 1
        file = bumblebee_root+str(num)+'.wav'
        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.tessa')
        engine.save_to_file(output, file)
        engine.runAndWait()
        playsound.playsound(file, True)
        os.remove(file)
        return

    '''Give user chance to repeat when bumblebee doesn't hear properly.'''    
    def infinite_speaking_chances(self, input_text):
        while input_text == '':
            input_text = self.hear().lower()
        return input_text

    '''Check for cancel command from user.'''    
    def interrupt_check(self, input_text):
        if "stop" in input_text or "cancel" in input_text:
            self.respond("Okay.")
            return True
