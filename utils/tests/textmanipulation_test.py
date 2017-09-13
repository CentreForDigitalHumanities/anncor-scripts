""""
    Testcases for the text manipulation file
"""

import unittest
from ..textmanipulation import *

class TestTextManipulation(unittest.TestCase):

    def test_datestring_to_timestamp(self):
        """
        Testing if the first and last month work correctly
        :return:
        """
        result = datestring_to_timestamp("01-JAN-1990")
        self.assertEqual(result, 631148400.0)
        result = datestring_to_timestamp("01-DEC-2000")
        self.assertEqual(result, 975625200.0)
