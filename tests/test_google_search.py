import unittest
from features import google_search
from unittest.mock import MagicMock
from unittest.mock import patch
from tests import MockBee

mock_bee = MockBee()
google_search_obj = google_search.Feature(mock_bee.bumblebee_api)


class TestGoogleSearch(unittest.TestCase):

    def test_search_function_called(self):
        input = "do a google search on my query"
        google_search_obj.search = MagicMock(return_value="my query")
        query = google_search_obj.action(input)
        google_search_obj.search.assert_called_once_with(
            input, google_search_obj.patterns)
        self.assertEquals(query, "my query")

    def test_browser_open_function_called(self):
        input = "do a google search of my query"
        with patch('webbrowser.open') as mock_wbopen:
            query = google_search_obj.action(input)
            mock_wbopen.assert_called_once_with(
                "https://google.com/search?q={}".format(query))


if __name__ == '__main__':
    unittest.main()
