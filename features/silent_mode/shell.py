#!python3

from features import configs as actions
from cmd import Cmd
import os

'''This is the listener for Bumblebee's CLI'''

'''Subclassing the Cmd class.'''
class MyPrompt(Cmd):
    input_placeholder="No input"
    prompt = 'how may I help you?> '
    intro = "Type ? for a list of all commands"
    def do_exit(self, input):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit Bumblebee. Shorthand: x q Ctrl-D.')
        
    def do_add(self, input):
        '''add a new entry to the Leslie.'''
        print("Adding '{}'".format(input))
        
    def do_youtube(self, input):
        '''open YouTube with specific search string.'''
        actions.youtube_search.action(str(input))
        
    def do_grepapp(self, input):
        '''open grep.app with specific search string.'''
        grepapp.search(input)
        print('Opened a grep.app search in a browser tab for you.')
        
    def do_google(self, input):
        '''do a Google search.'''
        actions.google_search.action(str(input))

    def do_wikipedia(self, input):
        '''do a wikipedia search.'''
        actions.wiki_search.action(str(input))
        
    def do_start_research(self):
        '''starts server for research.'''
        actions.start_research_server(input_placeholder)

    def do_store_research(self):
        '''stores data collected during research mode.'''
        actions.store_research_data(input_placeholder)

    def do_stop_research(self):
        '''stops the research server.'''
        actions.stop_research_server.action(input_placeholder)

    def do_send_email(self):
        '''starts a prompt to send an email to a desired user in the database.'''
        actions.send_email.action(input_placeholder)

    def do_clock_in(self):
        '''starts prompt to clock you in for an employer.'''
        actions.clock_in.action(input_placeholder)

    def do_clock_out(self):
        '''clocks you out of work.'''
        actions.clock_out.action(input_placeholder)

    def do_what_is(self, input):
        '''does math or general stat check using wolframalpha'''
        actions.wolfram_search.action(str(input))
        
    def do_hey(self, input):
        '''soon to be chat bot. Say bye to stop chatting'''
        actions.greet.action(str(input))

    def do_notepad(self):
        '''opens up bumblebee's notepad.'''
        actions.open_notepad.action(input_placeholder)

    def do_time(self):
        '''returns the current time.'''
        actions.get_time.action(input_placeholder)

    def do_add_zoom(self):
        '''opens a window to add a new zoom link to database.'''
        actions.add_zoom.action(input_placeholder)

    def open_zoom(self, input):
        '''opens a zoom link in browser window.'''
        actions.open_zoom.action(str(input))
        
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


def main():
    MyPrompt().cmdloop()
