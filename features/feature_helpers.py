'''Contains helper functions that can be used by any feature.'''


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
        query = Python

    This function also ignores false search_term_indicators such
    as 'like to', 'love to', 'want to'
    e.g. 'I want to do a google search on Python'
        false search term indicator = like
        search term = on
        query = Python

        Thus the function will correctly ignore 'like to google'
        as a possible search query and will capture 'Python' as
        the right query.

    Other exmaples of use cases: 'Send an email to Alex'


    Arguments: <string> spoken_text, <list> feature_patterns,
                <list> search_terms, <list> false_search_term_indicators
    Return type: <string> spoken_text (now stripped down to
    only the search query.)
    '''
    query_found = False

    for search_term in search_terms:
        if search_term in spoken_text:
            search_index = spoken_text.index(search_term)

            # ignore cases with "like to", "love to" "ready to"
            if spoken_text[search_index-1] in false_search_term_indicators:
                # looking for the search term in rest of text after
                # the false_search_term_indicator.
                search_index = spoken_text[
                    search_index+1:
                ].index(search_term)
            # get everything after the search term
            spoken_text = spoken_text[search_index+1:]
            query_found = True
            break

    # In case none of the search terms are included in spoken_text.
    if not query_found:
        for phrase in patterns:
            # split the phrase into individual words
            phrase_list = phrase.split(' ')
            # remove phrase list from spoken_text
            spoken_text = [
                word for word in spoken_text if word not in phrase_list
            ]

    spoken_text = ' '.join(spoken_text)
    # Need to remove whitespace before and after the wanted query.
    # This if useful for doing database searches on the query.
    spoken_text = spoken_text.strip()
    return spoken_text
