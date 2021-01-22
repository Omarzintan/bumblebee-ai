#!python3

import webbrowser

'''
Opens up google search in browser with search string.
Argument: <string> search
Return type: None
'''
def search(input):
    webbrowser.open('https://google.com/search?q={}'.format(input))
