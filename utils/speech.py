'''Functions responsible for Bumblebee's speech recognition and responding'''

import speech_recognition as sr
import playsound
import pyttsx3
from helpers import bumblebee_root
from colorama import Fore
from halo import Halo
from collections import deque


class BumbleSpeech():
    def __init__(self, speech_mode='voice'):
        self.spinner = Halo(spinner='dots')
        self.speech_modes = ['silent', 'voice']
        self.speech_mode = speech_mode
        self.engine = pyttsx3.init()
        self.engine.setProperty(
            'voice', 'com.apple.speech.synthesis.voice.tessa')
        self.engine.setProperty('rate', 210)
        self.input_queue = deque()
        self.YES_TERMS = [
            "yes",
            "sure",
            "yhup",
            "yup",
            "ye",
            "yeah",
        ]
        self.NO_TERMS = [
            "no",
            "nope",
            "nah",
            "nay",
        ]
        self.CANCEL_TERMS = [
            "stop",
            "cancel",
            "abort"
        ]

    def change_voice(self):
        '''Function to change voice of the voice engine'''
        # TODO
        return

    def change_speech_rate(self):
        '''Function to change the speaking rate'''
        # TODO
        return

    def set_input_queue(self, input_list: list):
        '''
        Function to set the input queue to be used to simulate user responses
        to Bumblebee. This is useful for programatically answering prompts when
        a feature is being run in a routine.
        Note: The input queue should have fewer or as many items as hear calls
        that the feature has. This will prevent items set by one feature to be
        encountered by other features which are called afterwards.
        '''
        self.input_queue = deque(input_list)

    def set_speech_mode(self, mode: str):
        '''Function to set speech mode.'''
        if not isinstance(mode, (str)):
            return -1
        mode = mode.lower()
        if mode in self.speech_modes:
            self.speech_mode = mode
        else:
            raise Exception(f'Could not find {mode} mode.')
            return -1
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
        # If there are items in the input queue, use the queue to provide
        # input to the feature which is seeking for input.
        if (len(self.input_queue) > 0):
            return self.input_queue.popleft()

        # For silent mode.
        if self.speech_mode == self.speech_modes[0]:
            input_text = input(Fore.WHITE + 'type your response here: ')
            return input_text

        # For voice mode.
        elif self.speech_mode == self.speech_modes[1]:
            self.spinner.start(
                text=(Fore.RED + "Wait for beep to start talking..."))
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                spoken_text = ''
                # breifly adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=1)
                playsound.playsound(
                    bumblebee_root+'sounds/tone-beep.wav', True)
                self.spinner.stop()
                self.spinner.start(text='Listening')
                audio = recognizer.listen(source)
                self.spinner.stop()
                try:
                    self.spinner.start('Recognizing')
                    spoken_text = recognizer.recognize_google(audio)
                    self.spinner.stop()

                    print(Fore.WHITE + 'You said, ' + spoken_text)
                except sr.UnknownValueError:
                    self.spinner.stop()
                    self.respond('Sorry I did not hear you, please repeat.')
                except sr.RequestError:
                    # This happens when there is no internet connection.
                    self.spinner.stop()
                    self.respond('No internet connection found.')
                    self.respond('Starting silent mode.')
                    self.set_silent_mode(True)
            return spoken_text

    def respond(self, output):
        ''' Respond to requests/questions.'''
        # If we are in silent mode or the input queue is being used.
        if self.speech_mode == self.speech_modes[0] or \
                len(self.input_queue) > 0:
            print(Fore.YELLOW + output)
            return

        # Voice mode
        elif self.speech_mode == self.speech_modes[1]:
            self.spinner.start(text=(Fore.YELLOW + output))
            self.engine.say(output)
            self.engine.runAndWait()
            self.spinner.stop_and_persist()
            return

    def interrupt_check(self, input_text):
        '''Check for cancel command from user.'''
        # TODO: use cancel terms here.
        if "stop" in input_text or "cancel" in input_text:
            self.respond("Okay.")
            return True

    def approve(self, question):
        '''
        Seek approval from user.
        e.g. user says yes/no to confirm question.
        Arguments: question i.e. the question to be approved by the user.
        Returns: True if the user approves
                False if the user disapproves
        '''
        self.respond(question)
        while True:
            answer = self.hear()
            if self.interrupt_check(answer):
                return False
            if answer in self.YES_TERMS:
                return True
            elif answer in self.NO_TERMS:
                return False
            else:
                self.respond("Please say yes or no.")
