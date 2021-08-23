import unittest
from features import feature_helpers


class TestFeatureHelpers(unittest.TestCase):

    def test_get_search_query(self):
        patterns = [
            'send an email',
            'send an email to',
            'google search',
            'show me on google',
            "wikipedia",
            "search wikipedia for",
            "look up on wikipedia"
        ]
        search_terms = ['to', 'on', 'for', 'search']
        false_search_term_indicators = ['want', 'like']
        spoken_text1 = 'send an email to Alex'
        spoken_text2 = 'Do a google search on Python'
        spoken_text3 = 'search wikipedia for my query'

        response1 = feature_helpers.get_search_query(
            spoken_text1, patterns, search_terms, false_search_term_indicators
        )
        response2 = feature_helpers.get_search_query(
            spoken_text2, patterns, search_terms, false_search_term_indicators
        )
        response3 = feature_helpers.get_search_query(
            spoken_text3, patterns, search_terms, false_search_term_indicators
        )

        self.assertEqual(response1, 'Alex')
        self.assertEqual(response2, 'Python')
        self.assertEqual(response3, 'my query')

    def test_false_search_indicators(self):
        patterns = [
            'send an email',
            'send an email to',
            'google search',
            'show me on google',
        ]
        search_terms = ['to', 'on']
        false_search_term_indicators = ['want', 'like']
        spoken_text1 = 'I want to send an email to Alex'
        spoken_text2 = 'I would like to do a google search on Python'

        response1 = feature_helpers.get_search_query(
            spoken_text1, patterns, search_terms, false_search_term_indicators
        )
        response2 = feature_helpers.get_search_query(
            spoken_text2, patterns, search_terms, false_search_term_indicators
        )

        self.assertEqual(response1, 'Alex')
        self.assertEqual(response2, 'Python')

    def test_no_search_query_given(self):
        patterns = [
            'send an email',
            'send an email to',
            'google search',
            'show me on google',
        ]
        search_terms = ['to', 'on']
        false_search_term_indicators = ['want', 'like']
        spoken_text1 = 'I want to send an email to'
        spoken_text2 = 'I would like to do a google search on'
        spoken_text3 = 'send an email'

        response1 = feature_helpers.get_search_query(
            spoken_text1, patterns, search_terms, false_search_term_indicators
        )
        response2 = feature_helpers.get_search_query(
            spoken_text2, patterns, search_terms, false_search_term_indicators
        )
        response3 = feature_helpers.get_search_query(
            spoken_text3, patterns, search_terms, false_search_term_indicators
        )

        self.assertEqual(response1, "")
        self.assertEqual(response2, "")
        self.assertEqual(response3, "")


if __name__ == '__main__':
    unittest.main()
