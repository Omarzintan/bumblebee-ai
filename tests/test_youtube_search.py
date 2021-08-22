import unittest
from features import youtube_search
from unittest.mock import MagicMock
from unittest.mock import patch
from tests import MockBee

mock_bee = MockBee()
youtube_search_obj = youtube_search.Feature(mock_bee.bumblebee_api)


class TestYoutubeSearch(unittest.TestCase):

    def test_search_function_called(self):
        input = "show me a video on youtube videos"
        youtube_search_obj.search = MagicMock(return_value="youtube videos")
        query = youtube_search_obj.action(input)
        youtube_search_obj.search.assert_called_once_with(
            input)
        self.assertEquals(query, "youtube videos")

    def test_browser_open_function_called(self):
        input = "show me a video on youtube videos"
        with patch('webbrowser.open') as mock_wbopen:
            query = youtube_search_obj.action(input)
            mock_wbopen.assert_called_once_with(
                "https://www.youtube.com/results?search_query='{}'".format(
                    query))


if __name__ == '__main__':
    unittest.main()
