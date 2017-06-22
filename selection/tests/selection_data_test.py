

import unittest

from selection.selection_problem_example.selection_data import SelectionData


class TestSelectionData(unittest.TestCase):

    def setUp(self):
        self.data = {}
        for y in range(1,6):
            self.data[y] = {}
            for m in range(1,13):
                if m == 6:
                    self.data[y][m] = {
                        "n_files": 100,
                        "n_annotated": 100
                    }
                else:
                    self.data[y][m] = {
                        "n_files": 10,
                        "n_annotated": 0
                    }
        self.selectionData = SelectionData(self.data)


    def test_get_random_from_year(self):
        month = self.selectionData.get_random_from_year(1)
        keys = [key for key in month]
        self.assertEqual(set(keys), set(["n_files", "n_annotated"]))
