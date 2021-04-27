'''Functions responsible for Bumblebee's speech recognition and responding'''

import speech_recognition as sr
import os
import sys
import playsound
import pyttsx3
from helpers import bumblebee_root
from colorama import Fore

silent_mode = False


class BumbleSpeech():

    def set_silent_mode(self, bool_val):
        '''Function to set silent mode.'''
        global silent_mode
        if not isinstance(bool_val, (bool)):
            return -1
        silent_mode = bool_val
        return 0

    def hear(self):
        ''' Function to capture requests/questions.'''
        if silent_mode:
            input_text = input(Fore.WHITE + 'type your response here: ')
            return input_text

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            spoken_text = ''
            # breifly adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            playsound.playsound(bumblebee_root+'sounds/tone-beep.wav', True)
            audio = recognizer.listen(source)
            try:
                spoken_text = recognizer.recognize_google(audio)
                print(Fore.WHITE + 'You said, ' + spoken_text)
            except sr.UnknownValueError:
                self.respond('Sorry I did not hear you, please repeat.')
            except sr.RequestError:
                # This happens when there is not internet connection.
                self.respond('No internet connection found.')
                self.respond('Starting silent mode.')
                self.set_silent_mode(True)
        return spoken_text

    def respond(self, output):
        ''' Respond to requests/questions.'''
        if silent_mode:
            print(Fore.YELLOW + output)
            return

        num = 0
        print(Fore.YELLOW + output)
        num += 1
        file = bumblebee_root+str(num)+'.wav'
        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.tessa')
        engine.save_to_file(output, file)
        engine.runAndWait()
        playsound.playsound(file, True)
        os.remove(file)
        return

    def infinite_speaking_chances(self, spoken_text):
        '''Give user chance to repeat when bumblebee doesn't hear properly.'''
        while spoken_text == '':
            spoken_text = self.hear().lower()
        return spoken_text

    def interrupt_check(self, spoken_text):
        '''Check for cancel command from user.'''
        if "stop" in spoken_text or "cancel" in spoken_text:
            self.respond("Okay.")
            return True
