'''Functions responsible for Bumblebee's speech recognition and responding'''

import speech_recognition as sr
import os
import playsound
import pyttsx3


class BumbleSpeech():
    ''' Function to capture requests/questions.'''
    def hear(self):
        input = sr.Recognizer()
        sr.energy_threshold = 4000 # makes adjusting to ambient noise more fine-tuned
        with sr.Microphone() as source:
            input.adjust_for_ambient_noise(source)
            playsound.playsound(os.environ.get('BUMBLEBEE_PATH')+'sounds/tone-beep.wav', True)
            audio = input.listen(source)
            data = ''
            try:
                data = input.recognize_google(audio)
                print('You said, ' + data)
            except sr.UnknownValueError:
                respond('Sorry I did not hear you, please repeat.')
        return data

    ''' Respond to requests/questions.'''
    def respond(self, output):
        num = 0
        print(output)
        num += 1
        file = os.environ.get('BUMBLEBEE_PATH')+str(num)+'.wav'
        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.tessa')
        engine.save_to_file(output, file)
        engine.runAndWait()
        playsound.playsound(file, True)
        os.remove(file)

