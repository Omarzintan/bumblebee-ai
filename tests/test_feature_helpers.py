import unittest
from features import feature_helpers


class TestFeatureHelpers(unittest.TestCase):

    def test_get_search_query(self):
        patterns = [
            'send an email',
            'send an email to',
            'google search',
            'show me on google'
            ]
        search_terms = ['to', 'on']
        false_search_term_indicators = ['want', 'like']

        spoken_text1 = 'send an email to Alex'
        spoken_text2 = 'I want to send an email to Alex'
        spoken_text3 = 'Do a google search on Python'
        spoken_text4 = 'I would like to do a google search on Python'

        response1 = feature_helpers.get_search_query(
            spoken_text1, patterns, search_terms, false_search_term_indicators
        )
        response2 = feature_helpers.get_search_query(
            spoken_text2, patterns, search_terms, false_search_term_indicators
        )
        response3 = feature_helpers.get_search_query(
            spoken_text3, patterns, search_terms, false_search_term_indicators
        )
        response4 = feature_helpers.get_search_query(
            spoken_text4, patterns, search_terms, false_search_term_indicators
        )
        self.assertTrue(response1, 'Alex')
        self.assertTrue(response2, 'Alex')
        self.assertTrue(response3, 'Python')
        self.assertTrue(response4, 'Python')


if __name__ == '__main__':
    unittest.main()
