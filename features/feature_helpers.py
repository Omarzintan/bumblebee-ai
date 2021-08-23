'''Contains helper functions that can be used by any feature.'''
from nltk_utils import tokenize


def get_search_query(
    spoken_text,
    patterns,
    search_terms,
    false_search_term_indicators=['like', 'love', 'want', 'ready']
):
    '''
    General function that extracts a search query from spoken
    text given search terms to look out for.
    Some possible search terms include 'to', 'on', 'for', 'about'
    e.g. 'do a google search on Python.'
        search term = on
        query found = Python

    This function also ignores false search_term_indicators such
    as 'like to', 'love to', 'want to'
    e.g. 'I want to do a google search on Python'
        false search term = to
        false search term indicator = want
        actual search term = on
        query found = Python

        Thus the function will correctly ignore 'do a google search on Python'
        as a possible search query and will capture 'Python' as
        the right query.

    Other exmaples of use cases: 'Send an email to Alex'
        search term = to
        query found = Alex

    Arguments: <string> spoken_text, <list> feature_patterns,
                <list> search_terms, <list> false_search_term_indicators
    Return type: <string> spoken_text (now stripped down to
    only the search query.)
    '''
    query_found = False
    query = ""
    # spoken_text from features is already in a tokenized form. If not, we
    # tokenize the text here.
    tokenized_text = spoken_text
    if isinstance(tokenized_text, str):
        tokenized_text = tokenize(spoken_text)
    has_search_term = any(
        search_term in tokenized_text for search_term in search_terms)
    while not query_found and has_search_term and tokenized_text != []:
        for search_term in search_terms:
            if search_term in tokenized_text:
                search_index = tokenized_text.index(search_term)
                # ignore cases with "like to", "love to" "ready to"
                if (tokenized_text[search_index-1] in
                        false_search_term_indicators):
                    phrase_after_false_term = tokenized_text[search_index+1:]
                    tokenized_text = phrase_after_false_term
                    break
                # get everything after the search term
                query = tokenized_text[search_index+1:]
                query_found = True
                break

    # In case none of the search terms are included in spoken_text.
    # This is just a fallback and is not expected to be used very often.
    if not query_found:
        tokenized_patterns = []
        for pattern in patterns:
            tokens = tokenize(pattern)
            tokenized_patterns.extend(tokens)
        query = [
            word for word in tokenized_text if word not in tokenized_patterns
        ]
    query = ' '.join(query)
    # Need to remove whitespace before and after the wanted query.
    # This if useful for doing database searches on the query.
    query = query.strip()
    return query
