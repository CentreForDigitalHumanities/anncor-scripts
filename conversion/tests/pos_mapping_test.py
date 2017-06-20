#!/usr/bin/env python3
"""
Test the mapping of a single POS node.
"""

import unittest
from ..pos_mapping import PosMapping, WordForm

TEST_FILE = "conversion/tests/files/pos_mapping_test.csv"

class PosMappingTest(unittest.TestCase):
    """
    Test the mapping of a single POS node.
    """

    def setUp(self):
        self.mapping = PosMapping()
        self.mapping.read(TEST_FILE)

    def test_lookup(self):
        """
        Tests that a mapping file in the expected format, is parsed as expected.
        """

        # Lines without a postfix
        self.assertEqual(
            ("PUNCT", WordForm.LEMMA, None),
            self.mapping["LET()"])
        self.assertEqual(
            ("ADV", WordForm.LEMMA, None),
            self.mapping["BW()"])

        # Lines with a postfix
        self.assertEqual(
            ("PRO:RED", WordForm.LEMMA, "-1PLNOM"),
            self.mapping["VNW(pers,pron,nomin,red,1,mv)"])
        self.assertEqual(
            ("V", WordForm.ROOT, "-INF"),
            self.mapping["WW(inf,vrij,zonder)"])

    def test_map(self):
        """
        Tests that a mapping returns an output as expected.
        """

        pos_node = MockPosNode(
            "WW(pv,tgw,mv)",
            "ga",
            "gaan")
        self.assertEqual("V|ga-PRES-PL", self.mapping.map(pos_node))

        pos_node = MockPosNode(
            "BW()",
            None,
            "zo")
        self.assertEqual("ADV|zo", self.mapping.map(pos_node))


class MockPosNode:
    """
    Mock representation of a word with an Alpino POS tag.
    """

    def __init__(self, tag, root, lemma):
        self.tag = tag
        self.lemma = lemma
        self.root = root
