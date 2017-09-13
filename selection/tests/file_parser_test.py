


import unittest

from selection.parser.file_parser import *


class TestFileParser(unittest.TestCase):

    def test_list_cha_files(self):
        result = set(list_cha_files("selection/tests/test_files"))
        expected = set(["test1.cha", "test2.cha", "test3.cha", "zipCha1.cha"])
        self.assertEqual(result, expected)

    def test_normalize_xml_files(self):
        result = get_cleaned_xml_files_in_path("selection/tests/test_files")
        expected = set(["test1", "test2"])
        self.assertEqual(result, expected)

    def test_get_date(self):
        result = get_date("@Date:	10-FEB-1988\n")
        self.assertEqual(result, "10-FEB-1988")

    def test_date_to_timestamp(self):
        result = datestring_to_timestamp("10-FEB-1988")
        self.assertEqual(result, 571446000)

    def test_file_to_number_and_name(self):
        file = "VanKampen_uttfiles2_Laura43_u0000028.xml"
        file2 = "VanKampen_Laura43_u00000100.xml"
        result = file_to_name_and_number(file)
        result2 = file_to_name_and_number(file2)
        self.assertEqual(result, ("Laura43", 28))
        self.assertEqual(result2, ("Laura43", 100))

    def test_get_number_from_file(self):
        file = "VanKampen_uttfiles2_Laura43_u0000028"
        file2 = "VanKampen_laura43_u00000100"
        result = get_number_from_file(file)
        result2 = get_number_from_file(file2)
        self.assertEqual(result,28)
        self.assertEqual(result2, 100)


