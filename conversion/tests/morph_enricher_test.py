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

MISSING_MAPPING = "conversion/tests/files/morph_enricher_missing_mapping.csv"
MISSING_CHAT = "conversion/tests/files/morph_enricher_missing.cha"
MISSING_CHAT_EXPECTED = "conversion/tests/files/morph_enricher_missing_expected.cha"
MISSING_LASSY = "conversion/tests/files/morph_enricher_missing.xml"


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

    def test_missing(self):
        """
        Test that a missing POS tag mapping is detected and returned as expected.
        """

        self.assertFalse(self.morph_enricher.has_failures)
        mapped = list(self.morph_enricher.map(MISSING_CHAT, MISSING_LASSY))

        with open(MISSING_CHAT_EXPECTED) as expected:
            self.assertSequenceEqual(
                list(line.rstrip('\n') for line in expected),
                mapped)

        self.assertTrue(self.morph_enricher.has_failures)
        self.assertEqual(1, self.morph_enricher.failed_sentences_count)
        self.assertSetEqual({"FOOBAR"}, self.morph_enricher.missing_tags)
