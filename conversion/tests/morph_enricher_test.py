#!/usr/bin/env python3
"""
Test the morphological enriching.
"""

import unittest
from ..morph_enricher import MorphEnricher
from ..pos_mapping import PosMapping
from ..punctuation_mapping import PunctuationMapping

MAPPING_FILE = "conversion/tests/files/morph_enricher_mapping.csv"
PUNCTUATION_FILE = "conversion/tests/files/punctuation_mapping_test.csv"
MAT21022_SAMPLE_CHAT = "conversion/tests/files/mat21022_sample.cha"
MAT21022_SAMPLE_CHAT_EXPECTED = "conversion/tests/files/mat21022_sample_expected.cha"
MAT21022_SAMPLE_LASSY = "conversion/tests/files/mat21022_sample.xml"


class MorphEnricherTest(unittest.TestCase):
    """
    Test the morphological enriching.
    """

    def setUp(self):
        mapping = PosMapping(PunctuationMapping(PUNCTUATION_FILE))
        mapping.read(MAPPING_FILE)
        self.morph_enricher = MorphEnricher(mapping)

    def test_mat21022_sample(self):
        """
        Test enriching a sample case.
        """

        with open(MAT21022_SAMPLE_CHAT_EXPECTED) as expected:
            self.assertSequenceEqual(
                list(line.rstrip('\n') for line in expected),
                list(self.morph_enricher.map(MAT21022_SAMPLE_CHAT, MAT21022_SAMPLE_LASSY)))
