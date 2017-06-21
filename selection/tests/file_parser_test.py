


import unittest
from ..file_parser import *

class TestFileParser(unittest.TestCase):

    def test_list_cha_files(self):
        result = set(list_cha_files("selection/tests/test_files"))
        expected = set(["test1.cha", "test2.cha", "test3.cha", "zipCha1.cha"])
        self.assertEqual(result, expected)

    def test_normalize_xml_files(self):
        result = normalize_xml_files("selection/tests/test_files")
        expected = set(["test1", "test2"])
        self.assertEqual(result, expected)

    def test_get_date(self):
        result = get_date("@Date:	10-FEB-1988\n")
        self.assertEqual(result, "10-FEB-1988")

    def test_date_to_timestamp(self):
        result = date_to_timestamp("10-FEB-1988")
        self.assertEqual(result, 571446000)