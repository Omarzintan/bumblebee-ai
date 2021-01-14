#!python3
import requests
import speech_recognition as sr # for converting speech to text
import os # to save/open files
import subprocess, signal
import logging, selectors
import sys
import playsound # to play saved mp3 file
import datetime # for fetching date and time
import time
import json
import difflib
import pprint
import pyttsx3 # gives Bumblebee a voice
import wikipedia
import wolframalpha # to calculate strings into formula
import ezgmail
from database import wolframalpha_key as wak
from threading import Thread
from features import grepapp
from features import youtube
from features import google
from features import greeting
from features import contacts
from features import shell
from features import myemail
from features import mynotepad
from features import research
from features import employment
from features import wake_word_detector

''' Function to capture requests/questions.'''
def talk():
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
def respond(output):
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

'''Check for cancel command from user.'''    
def interrupt_check(input):
    if "stop" in input or "cancel" in input:
        respond("Okay.")
        return True

'''Give user chance to repeat when bumblebee doesn't hear properly.'''    
def infinite_speaking_chances(input):
    while input == '':
        input = talk().lower()
    return input

'''Starts the flask server for research mode.'''
def start_server():
    global server_proc
    
    logging.basicConfig(filename=os.environ.get('BUMBLEBEE_PATH')+'server.log', level=logging.INFO)

    # log the date and time in log file
    logging.info(datetime.datetime.now().strftime('%d:%m:%Y, %H:%M:%S'))
    # Create the subprocess for the flask server.
    server_proc = subprocess.Popen([os.environ.get('PYTHON3_ENV'), os.environ.get('BUMBLEBEE_PATH')+'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
                   
    # Logging stdout and stderr from flask server in a way that preserves order.
    sel = selectors.DefaultSelector()
    sel.register(server_proc.stdout, selectors.EVENT_READ)
    sel.register(server_proc.stderr, selectors.EVENT_READ)

    while True:
        for key, _ in sel.select():
            data = key.fileobj.read1().decode()
            if not data:
                exit()
            if key.fileobj is server_proc.stdout:
                # Send stdout to log file
                logging.info(data)                
            else:
                # Send stderr to log file
                logging.info(data)

def stop_server():
    global server_proc
    os.killpg(os.getpgid(server_proc.pid), signal.SIGTERM)
    server_proc = ''
    print('Server stopped')

'''Wake bumblebee up.'''
def turn_on():
    global quit_interrupt
    global keep_listening
    global stop_listening
    global root
    respond('Hey.')
    while(1):
        respond('How may I help you?')
        text = ''
        text = infinite_speaking_chances(text)

        if 'done' in text or 'exit' in text or 'bye' in text:
            respond('Ok. I\'ll be listening for your command.')
            break

        if 'wikipedia' in text:
            respond('Searching Wikipedia')
            text = text.replace('wikipedia', '')
            try:
                results = wikipedia.summary(text, sentences = 3)
                respond('According to Wikipedia')
                respond(results)
            except:
                respond('I could not find anything related to your search on Wikipedia.')
          
        elif 'time' in text:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            respond(f'the time is {strTime}')

        elif 'google' in text:
            text = text.replace('search', '')
            text = text.replace('google', '')
            google.search(text)
            respond('I have opened a browser window with your search on {}.'.format(text))

        elif 'calculate' in text  or 'what is' in text:
            question = text.replace('calculate','')
            question = text.replace('what is', '')
            app_id = wak.get_key()
            client = wolframalpha.Client(app_id)
            try:
                res = client.query(question)
                answer = next(res.results).text
                respond('The answer is ' + answer)
            except:
                try:
                    answer = wikipedia.summary(question, sentences = 2)
                    respond('According to Wikipedia')
                    respond(answer)
                except:
                    respond('Sorry I could not perform your search.')

        elif 'youtube' in text:
            text = text.replace('youtube', '')
            youtube.search(text)
            respond('I have opened Youtube with a search on {}'.format(text))

        elif 'hello' in text or 'what\'s up' in text or 'hey' in text:
            respond(greeting.greet(text))

        elif 'about yourself' in text:
            response = 'My name is Bumblebee. I am Zintan\'s assistant.'
            response += 'I can do many things such as telling the time, '
            response += 'googling information, doing math, and opening Youtube.'
            response += 'I can also clock you into work as well as track your '
            response += 'browser activity in Google Chrome if you say Research Mode.'
            response += 'Look at the list of commands to help.'
            list_of_commands = {
                'google search': 'Example: "google something"',
                'time': 'Example: "what time is it?"',
                'youtube': 'Example: "Youtube Ghana"',
                'math and fun numerical facts': 'Example: "calculate 2 + 2 Or what is 2 + 2"',
                'email': 'Example: "send email"',
                'initiate research tracking': 'Example: "research mode"',
                'store research date': 'Example: "store data"',
                'stop research mode': 'Example: "stop research mode"'
            }
            respond(response)
            pprint.pprint(list_of_commands)

        elif 'notepad' in text:
            mynotepad.notepad()
            
        elif 'add email contact' in text:
            respond('What is the name of the contact.')
            name = talk()
            respond('Please type the email address of the contact.')
            email = input('type it here.')
            
        elif 'send email' in text:
            # get name of email contact
            respond('Who do you want to send the email to?')
            name = ''
            name = infinite_speaking_chances(name)
            if interrupt_check(name):                
                continue
            close_names = []
            while close_names == []:
                close_names = difflib.get_close_matches(name, contacts.get_names())
                if close_names == []:
                    respond('Could not find this contact. Please try again')
                    name = ''
                    name = infinite_speaking_chances(name)
                    if interrupt_check(name):
                        break
            try:
                recipient = contacts.get_email(close_names[0])
                print(recipient)
            except:
                respond("I will cease trying to send an email now.")
                continue
            # get subject
            respond('What is the subject of your email?')
            subject = ''
            subject = infinite_speaking_chances(subject)
            if interrupt_check(subject):
                continue
            # get message
            respond('What is the message of your email?')
            message = ''
            message = infinite_speaking_chances(message)
            if interrupt_check(message):
                continue
            # show email
            respond('Here is a summary of your email:')
            print(myemail.summary_email(recipient, subject, message))

            # edit email
            respond('Would you like to edit this?')
            edit = ''
            edit = inifinite_speaking_chances(edit)
            if interrupt_check(edit):
                continue
            if 'yes' in edit or 'yeah' in edit:
                edited_email = myemail.email_edit(recipient, subject, message)
                edited_email_json = json.loads(edited_email)
                recipient = edited_email_json["recipient"]
                subject = edited_email_json["subject"]
                message = edited_email_json["message"]
                respond('Here is another summary of your email:')
                print(myemail.summary_email(recipient, subject, message))
            respond('Would you like to send this email?')
            approve = ''
            approve = infinite_speaking_chances(approve)
            if interrupt_check(approve):
                continue
            if approve == 'yes':
                # send email
                ezgmail.init()
                message += "\n Bumblebee (Zintan's ai assistant)"
                ezgmail.send(recipient, subject, message)
                respond('I have sent the email.')
            else:
                respond('Okay.')

        elif 'stop research mode' in text:
            respond('Stopping research server.')
            stop_server()
            
        elif 'research mode' in text:
            global research_topic
            respond('What is the topic of your research?')
            topic = ''
            topic = infinite_speaking_chances(topic)
            if interrupt_check(topic):
                continue
            respond('Starting research mode on {}'.format(topic))
            respond('Would you like to edit this?')
            edit = ''
            edit = infinite_speaking_chances(edit)
            if interrupt_check(edit):
                continue
            if 'yes' in edit or 'yeah' in edit:
                edited_topic = research.topic_edit(topic)
                edited_json = json.loads(edited_topic)
                topic = edited_json["topic"]
                respond('Starting server for research on {}'.format(topic))
            research_topic = topic
            # start python flask server in new thread
            Thread(target=start_server).start()
        
        elif 'open shell' in text:
            shell.MyPrompt().cmdloop()

        elif 'store data' in text:
            respond('Storing research data.')
            try:
                filename = research_topic
                filename = filename.replace(' ', '-')
                print(filename)
                res = requests.post(os.environ.get('SERVER_URL')+'/store_data', params={'filename': filename})
                res.raise_for_status()
                respond('Research data stored successfully at {}.txt'.format(filename))
            except:
                respond('Failed to store research data.')
            
        elif 'clock me in' in text:
            global currently_working
            global employer
            global work_start_time

            respond('Is this for Peggy or Osborn?')
            employer = ''
            employer = infinite_speaking_chances(employer)
            if interrupt_check(employer):
                continue
            close_names = []
            while close_names == []:
                close_names = difflib.get_close_matches(employer, ['peggy', 'osborn'])
                if close_names == []:
                    respond('I don\'t know this employer. Please try again')
                    employer = ''
                    employer = infinite_speaking_chances(employer)
                    if interrupt_check(employer):
                        break
            employer = close_names[0]
            if 'peggy' in employer:
                employer = 'peggy'
                work_start_time = datetime.datetime.now()
                currently_working = True
                # access peggy file and put timestamp there
                employment.clock_in(employer, work_start_time.strftime('%d:%m:%Y, %H:%M:%S'))
                respond('You\'ve been clocked in for {}.'.format(employer))
                print(work_start_time, currently_working)
                pass
            elif 'osborn' in employer:
                # access osborn file and put timestamp there
                employer = 'osborn'
                work_start_time = datetime.datetime.now()
                currently_working = True
                employment.clock_in(employer, work_start_time.strftime('%d-%m-%Y, %H:%M:%S'))
                respond('You\'ve been clocked in for {}.'.format(employer))
            
        elif 'clock me out' in text:
            if not currently_working:
                respond('You\'ve not been clocked in.')
                continue
            currently_working = False
            work_stop_time = datetime.datetime.now()
            duration = (work_stop_time - work_start_time)
            print(duration)
            employment.clock_out(employer, work_stop_time.strftime('%d-%m-%Y, %H:%M:%S'), duration)
            respond('You\'ve been clocked out.')
        
        elif 'stop listening' in text:
            respond('To get me back you will have to boot me back up. Are you sure?')
            approve = ''
            approve = infinite_speaking_chances(approve)
            if interrupt_check(approve):
                continue
            if 'yes' in approve:
                respond('See you later then, bye. Take care.')
                if server_proc:
                    stop_server()
                if currently_working:
                    work_stop_time = datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
                    duration = str(int(work_stop_time) - int(work_start_time)).strftime('%H:%M:%S')
                    employment.clock_out(employer, work_stop_time, duration)
                wake_word_detector.stop()
            else:
                respond('Alright, I will not stop.')

        else:
            respond('I do not know how to do this yet.')
        
if __name__ == '__main__':    
    global research_topic
    global server_proc
    global currently_working
    global employer
    global work_start_time
    
    server_proc=''
    currently_working=''
    while(1):
        if wake_word_detector.run():
            turn_on()
