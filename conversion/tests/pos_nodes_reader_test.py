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
        with open(TEST_FILE) as test_file:
            sentences = list(self.reader.read_sentences(test_file))

        self.assertEqual(1,
                         len(sentences),
                         "The sentence should have been found")

        sentence = sentences[0]
        self.assertEqual("Leden van de Staten-Generaal ,",
                         sentence.sentence_text)
        self.assertSequenceEqual(
            ["Leden", "van", "de", "Staten-Generaal", ","],
            list(node.word for node in sentence.pos_nodes))

    def test_read_multiple(self):
        """
        Test whether reading a file with multiple sentences works as expected.
        """
        with open(TEST_FILE2) as test_file2:
            sentences = list(self.reader.read_sentences(test_file2))

        expected_sentences = [
            "nee , we gaan zo pindaatjes rijgen .",
            "ik ik heeft gespuugd in bed !",
            "dan kunnen we straks nog wel kijken of we nog een leuk boekje kunnen vinden ."]

        self.assertEqual(
            len(expected_sentences),
            len(sentences),
            "The sentences should have been found")

        for (expected_sentence, sentence) in zip(expected_sentences, sentences):
            self.assertEqual(expected_sentence, sentence.sentence_text)
            self.assertSequenceEqual(
                expected_sentence.split(" "),
                list(node.word for node in sentence.pos_nodes))
