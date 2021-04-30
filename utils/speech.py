'''Functions responsible for Bumblebee's speech recognition and responding'''

import speech_recognition as sr
import os
import sys
import playsound
import pyttsx3
from helpers import bumblebee_root
from colorama import Fore
from halo import Halo


class BumbleSpeech():
    def __init__(self):
        self.listening_spinner = Halo(text='Listening', spinner='dots')
        self.recognize_spinner = Halo(text='Recognizing', spinner='dots')
        self.silent_mode = False

    def set_silent_mode(self, bool_val):
        '''Function to set silent mode.'''
        if not isinstance(bool_val, (bool)):
            return -1
        self.silent_mode = bool_val
        return 0

    def infinite_speaking_chances(func):
        '''
        Wrapper for bumblebee hear function.
        This wrapper gives the user a chance to repeat
        when bumblebee doesn't hear properly.
        '''
        def wrapper(*args, **kwargs):
            input_text = ''
            while input_text == '':
                input_text = func(*args, **kwargs)
            return input_text
        return wrapper

    @infinite_speaking_chances
    def hear(self):
        '''
        Function to capture requests/questions.
        '''

        if self.silent_mode:
            input_text = input(Fore.WHITE + 'type your response here: ')
            return input_text

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            spoken_text = ''
            # breifly adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            playsound.playsound(bumblebee_root+'sounds/tone-beep.wav', True)
            self.listening_spinner.start()
            audio = recognizer.listen(source)
            self.listening_spinner.stop()
            try:
                self.recognize_spinner.start()
                spoken_text = recognizer.recognize_google(audio)
                self.recognize_spinner.stop()

                print(Fore.WHITE + 'You said, ' + spoken_text)
            except sr.UnknownValueError:
                self.recognize_spinner.stop()
                self.respond('Sorry I did not hear you, please repeat.')
            except sr.RequestError:
                # This happens when there is not internet connection.
                self.recognize_spinner.stop()
                self.respond('No internet connection found.')
                self.respond('Starting silent mode.')
                self.set_silent_mode(True)
        return spoken_text

    def respond(self, output):
        ''' Respond to requests/questions.'''
        if self.silent_mode:
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

    def interrupt_check(self, input_text):
        '''Check for cancel command from user.'''
        if "stop" in input_text or "cancel" in input_text:
            self.respond("Okay.")
            return True
