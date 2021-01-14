#!python3

from cmd import Cmd
import os

'''This is bumblebee's shell'''

# Subclassing the Cmd class. This is the CLI aspect of Leslie
class MyPrompt(Cmd):
    prompt = 'k> '
    intro = "Hi I am Leslie! Type ? to list my commands"
    def do_exit(self, input):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit Leslie. Shorthand: x q Ctrl-D.')
        
    def do_add(self, input):
        '''add a new entry to the Leslie.'''
        print("Adding '{}'".format(input))
        
    def do_youtube(self, input):
        '''open YouTube with specific search string.'''
        youtube.search(input)
        print('Opened a youtube search in a browser tab for you.')
        
    def do_grepapp(self, input):
        '''open grep.app with specific search string.'''
        grepapp.search(input)
        print('Opened a grep.app search in a browser tab for you.')
        
    def do_google(self, input):
        '''do a Google search.'''
        google.search(input)
        print('Opened a google search in a browser tab for you.')

    def do_hey(self, input):
        '''soon to be chat bot. Say bye to stop chatting'''
        greeting.greet(input)
    def do_shell(self, input):
        '''run shell command'''
        stream = os.popen(input)
        output = stream.read()
        print(output)
    def default(self, input):
        if input == 'x' or input == 'q' or input == 'bye':            
            return self.do_exit(input)
        print("Default: {}".format(input))

    do_EOF = do_exit
    help_EOF = help_exit
