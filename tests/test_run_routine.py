import unittest
from features import run_routine
from tests import MockBee

mock_bee = MockBee()
run_routine_obj = run_routine.Feature(mock_bee.bumblebee_api)


class TestRunRoutine(unittest.TestCase):
    def test_process_routine_file(self):
        tags_list, arguments_list = run_routine_obj.process_routine_file(
            "tests/test_data/fake_routine_file.txt")
        self.assertEquals(tags_list,
                          ["google_search", "youtube_search", "send_email"])
        self.assertEquals(arguments_list,
                          [["kobe", "steph", "giannis"],
                           ["python", "java", "kotlin"],
                           ["zintan", "subject", "message", "no", "yes"]])


if __name__ == '__main__':
    unittest.main()
