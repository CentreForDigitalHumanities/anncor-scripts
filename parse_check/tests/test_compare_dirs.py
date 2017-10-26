import unittest
from parse_check.compare_dirs import *


class TestCompareDirs(unittest.TestCase):
    def setUp(self):
        self.dir_1 = "./parse_check/tests/files/dir_1"
        self.dir_2 = "./parse_check/tests/files/dir_2"
        self.selection = lambda x: ".xml" in x
        self.tags = ["tag1", "tag2"]
        self.ignore_characters = [".", "\n", " "]

    def test_compare_dirs(self):
        dir_1 = self.dir_1
        dir_2 = self.dir_2
        selection = self.selection
        tags = self.tags
        ignore_characters = self.ignore_characters
        result = compare_dirs(dir_1, dir_2, selection, tags, ignore_characters)
        self.assertEqual(
            result,
            [
                {"file": "2.xml", "problem": "Tags have difference",
                 "problem_detail": {"tag1": [("a", "i")], "tag2": [(None, "!")]},
                 "locations": [self.dir_1, self.dir_2]},
                {"file": "3.xml", "problem": "No match in dir 2", "problem_detail": None, "locations": [self.dir_1]},
                {"file": "4.xml", "problem": "No match in dir 1", "problem_detail": None, "locations": [self.dir_2]},
            ]
        )

    def test_compare_files(self):
        files_1 = sort_splited_paths_on_filename(split_paths(list_files(self.dir_1, self.selection)))
        files_2 = sort_splited_paths_on_filename(split_paths(list_files(self.dir_2, self.selection)))
        result = compare_files(files_1, files_2, self.tags, self.ignore_characters)

        self.assertEqual(
            result,
            [
                {"file": "2.xml", "problem": "Tags have difference",
                 "problem_detail": {"tag1": [("a", "i")], "tag2": [(None, "!")]},
                 "locations": [self.dir_1, self.dir_2]},
                {"file": "3.xml", "problem": "No match in dir 2", "problem_detail": None, "locations": [self.dir_1]},
                {"file": "4.xml", "problem": "No match in dir 1", "problem_detail": None, "locations": [self.dir_2]},
            ]
        )

