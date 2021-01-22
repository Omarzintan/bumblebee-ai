#!python3

import webbrowser

'''
Opens YouTube in a browser with the specified search query.
Argument: <string> input
Return type: None
'''
def search(input):
    webbrowser.open("https://www.youtube.com/results?search_query='{}'".format(input))
