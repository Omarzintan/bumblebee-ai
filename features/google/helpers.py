import webbrowser

'''
Parses spoken text to retrieve a search query for Google
Argument: <string> spoken_text, <list> keywords
Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.
'''
def get_search_query(spoken_text, keywords):
    for word in keywords:
        spoken_text = spoken_text.replace(word, '')
    return spoken_text

'''
Opens up google search in browser with search string.
Argument: <string> spoken_text, <list> keywords
Return type: <string> query
'''
def search(spoken_text, keywords):
    query = get_search_query(spoken_text, keywords)
    webbrowser.open("https://google.com/search?q={}".format(query))
    return query

