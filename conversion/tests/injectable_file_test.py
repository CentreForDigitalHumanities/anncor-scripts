"""
Test the injectable file modifier.
"""

import unittest
from ..injectable_file import InjectableFile

TEST_FILE = "conversion/tests/files/injectable_test.txt"
EXPECTED_LINES = ["Line {0}".format(i) for i in range(1, 11)]

class InjectableFileTest(unittest.TestCase):
    """
    Test the injectable file modifier.
    """
    def setUp(self):
        self.file = InjectableFile(TEST_FILE)

    def tearDown(self):
        self.file.close()

    def test_read(self):
        """
        Test that reading a file without modifications, works as expected.
        """
        self.assertSequenceEqual(EXPECTED_LINES, list(self.file.read_lines()))

    def test_modification(self):
        """
        Test that modifications to a file are placed as expected.
        """
        self.file.append_at(4, "Hallo")
        self.file.append_at(7, "Hello")

        expected_modified_lines = list(EXPECTED_LINES)
        expected_modified_lines.insert(8, "Hello")
        expected_modified_lines.insert(5, "Hallo")

        self.assertSequenceEqual(expected_modified_lines, list(self.file.read_lines(True)))
