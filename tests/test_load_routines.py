import unittest
from features import load_routines
from tests import MockBee
from tinydb import TinyDB, Query

mock_bee = MockBee()
load_routines_obj = load_routines.Feature(mock_bee.bumblebee_api)


class TestLoadRoutines(unittest.TestCase):

    def test_load_routines(self):
        fake_routines_db = TinyDB("tests/test_data/fake_routines_db.json")
        load_routines_obj.update_routines_database(
            "tests/test_data/", fake_routines_db)
        Item = Query()
        db_entry = fake_routines_db.search(Item.name == "fake routine")[0]
        self.assertEquals(db_entry["name"], "fake routine")
        self.assertEquals(db_entry["filepath"],
                          "tests/test_data/fake_routine_file.txt")


if __name__ == '__main__':
    unittest.main()
