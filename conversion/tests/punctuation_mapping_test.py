#!/usr/bin/env python3
"""
Tests the punctuation mapping.
"""

import unittest
from ..punctuation_mapping import PunctuationMapping

TEST_FILE = "conversion/tests/files/punctuation_mapping_test.csv"


class PunctuationMappingTest(unittest.TestCase):
    """
    Tests the punctuation mapping.
    """

    def setUp(self):
        self.punctuation_mapping = PunctuationMapping(TEST_FILE)

    def test_punctuation_mapping(self):
        """
        Test that punctuation symbols can be mapped to a written out variant.
        """
        self.assertEqual(
            "period",
            self.punctuation_mapping['.'])

        self.assertEqual(
            "cm",
            self.punctuation_mapping[','])
