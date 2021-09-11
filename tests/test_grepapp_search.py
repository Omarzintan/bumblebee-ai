import unittest
from features import grepapp_search
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import call
from tests import MockBee

mock_bee = MockBee()
grepapp_search_obj = grepapp_search.Feature(mock_bee.bumblebee_api)


class TestGrepappSearch(unittest.TestCase):

    def test_search_function_called(self):
        input = "search github for this repository"
        grepapp_search_obj.search = MagicMock(return_value="this repository")
        query = grepapp_search_obj.action(input)
        grepapp_search_obj.search.assert_called_once_with(query)
        self.assertEquals(query, "this repository")

    def test_search_with_arguments_list(self):
        arguments_list = ["python", "java", "c++", "kotlin"]
        grepapp_search_obj.search = MagicMock()
        grepapp_search_obj.action("", arguments_list)
        # TODO: fix test
        grepapp_search_obj.search.assert_has_calls([
            call("python"), call("java"), call("c++"), call("kotlin")],
            any_order=False)

    def test_browser_open_function_called(self):
        input = "search github for this repository"
        with patch('webbrowser.open') as mock_wbopen:
            query = grepapp_search_obj.action(input)
            mock_wbopen.assert_called_once_with(
                "https://grep.app/search?q={}".format(query))


if __name__ == '__main__':
    unittest.main()
