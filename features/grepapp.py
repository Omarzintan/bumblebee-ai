#!python3

import webbrowser

'''
Opens up a grep.app search in browser.
Argument: <string> input i.e. the search query
Return type: None
'''
def search(input):
    webbrowser.open('https://grep.app/search?q={}'.format(input))

