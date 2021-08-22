import unittest
from features import wiki_search
from unittest.mock import MagicMock
from unittest.mock import patch
from tests import MockBee
import wikipedia

mock_bee = MockBee()
wiki_search_obj = wiki_search.Feature(mock_bee.bumblebee_api)


class TestWikiSearch(unittest.TestCase):

    def test_summary_function_called(self):
        input = "search wikipedia about my query"
        mock_bee.speech.respond = MagicMock(return_value="Respond called")
        with patch('wikipedia.summary') as mock_wiki_summary:
            wiki_summary_result = "Wikipedia summary about query found"
            mock_wiki_summary.return_value = wiki_summary_result
            wiki_search_obj.action(input)
            mock_wiki_summary.assert_called_once_with("my query", sentences=2)
            wiki_search_obj.bs.respond.assert_called_with(
                "According to Wikipedia, " + wiki_summary_result)

    def test_throws_wikipedia_Page_Error(self):
        input = "search wikipedia for"
        mock_bee.speech.respond = MagicMock(return_value="Respond called")
        with patch('wikipedia.summary') as mock_wiki_summary:
            mock_wiki_summary.side_effect = wikipedia.exceptions.PageError(
                'mock_wiki_summary')
            wiki_search_obj.action(input)
            mock_wiki_summary.assert_called_once_with("", sentences=2)
            wiki_search_obj.bs.respond.assert_called_once_with(
                "I could not find any pages "
                "related to your search.")


if __name__ == '__main__':
    unittest.main()
