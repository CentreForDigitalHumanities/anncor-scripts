import unittest
from utils.xml import *

class TestXml(unittest.TestCase):

    def setUp(self):
        self.file_ref_1 = "./utils/tests/test_files_xml/test_file_1.xml"
        self.file_ref_2 = "./utils/tests/test_files_xml/test_file_2.xml"


    def test_compare_xml_tag(self):
        result = compare_xml_tag(self.file_ref_1, self.file_ref_2, "tag1", [" ", "\n"])
        self.assertEqual(result, [])
        result = compare_xml_tag(self.file_ref_1, self.file_ref_2, "tag2")
        self.assertEqual(len(result), 1)

        result = compare_xml_tag(self.file_ref_1, self.file_ref_2, "tag2", ["."])
        self.assertEqual(result, [])

    def test_compare_two_xml_tags(self):
        result = compare_two_xml_tag(self.file_ref_1, self.file_ref_2, "tag1", "tag3", [".", " "])
        self.assertEqual(len(result), 1)

    def test_trim_text(self):
        text = "this is a text"
        result = trim_text(text)
        self.assertEqual(result, text)
        result = trim_text("......this is a text", ["."])
        self.assertEqual(result, text)
