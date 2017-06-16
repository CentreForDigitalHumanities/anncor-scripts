#!/usr/bin/env python3
"""
Test the POS nodes reader.
"""

import unittest
from ..pos_nodes_reader import PosNodesReader

TEST_FILE = "conversion/tests/files/s1.xml"
TEST_FILE2 = "conversion/tests/files/s2.xml"

class PosNodesReaderTest(unittest.TestCase):
    """
    Test the POS nodes reader.
    """
    def setUp(self):
        self.reader = PosNodesReader()

    def test_read_single(self):
        """
        Test whether reading a file with one sentence works as expected.
        """
        sentences = list(self.reader.read_sentences(TEST_FILE))

        self.assertEqual(1,
                         len(sentences),
                         "The sentence should have been found")

        (sentence, pos_nodes) = sentences[0]
        self.assertEqual("Leden van de Staten-Generaal ,", sentence)
        self.assertSequenceEqual(
            ["Leden", "van", "de", "Staten-Generaal", ","],
            list(node.word for node in pos_nodes))

    def test_read_multiple(self):
        """
        Test whether reading a file with multiple sentences works as expected.
        """
        sentences = list(self.reader.read_sentences(TEST_FILE2))

        expected_sentences = [
            "nee , we gaan zo pindaatjes rijgen .",
            "ik ik heeft gespuugd in bed !",
            "dan kunnen we straks nog wel kijken of we nog een leuk boekje kunnen vinden ."]

        self.assertEqual(
            len(expected_sentences),
            len(sentences),
            "The sentences should have been found")

        for (expected_sentence, (sentence, pos_nodes)) in zip(expected_sentences, sentences):
            self.assertEqual(expected_sentence, sentence)
            self.assertSequenceEqual(
                expected_sentence.split(" "),
                list(node.word for node in pos_nodes))
