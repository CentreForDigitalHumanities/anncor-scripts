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
        mock_punctuation = {
            ';': "semicolon",
            ':': "colon",
            '.': "period",
            ',': "cm",
            '!': "exclamation",
            '?': "question",
            "“": "bq",
            "”": "eq"
        }

        self.mapping = PosMapping(mock_punctuation)
        self.mapping.read(TEST_FILE)

    def test_lookup(self):
        """
        Test that a mapping file in the expected format, is parsed as expected.
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
        Test that a mapping returns an output as expected.
        """

        pos_node = MockPosNode(
            "WW(pv,tgw,mv)",
            "ga",
            "gaan",
            "gaan")
        self.assertEqual("V|ga-PRES-PL", self.mapping.map(pos_node))

        pos_node = MockPosNode(
            "BW()",
            None,
            "zo",
            "zo")
        self.assertEqual("ADV|zo", self.mapping.map(pos_node))

    def test_map_quotes(self):
        """
        Test that quotation marks are converted to “smart” quotes and properly converted.
        """

        pos_node = MockPosNode(
            "LET()",
            '"',
            '"',
            '"')
        state = {}
        self.assertEqual("bq|bq", self.mapping.map(pos_node, state))
        self.assertEqual("eq|eq", self.mapping.map(pos_node, state))
        self.assertEqual("bq|bq", self.mapping.map(pos_node, state))

        # new state
        self.assertEqual("bq|bq", self.mapping.map(pos_node))

        # test that an already encoded document is parsed as is
        pos_node = MockPosNode(
            "LET()",
            "“",
            "“",
            "“")

        self.assertEqual("bq|bq", self.mapping.map(pos_node, state))
        self.assertEqual("bq|bq", self.mapping.map(pos_node, state))

        pos_node = MockPosNode(
            "LET()",
            "”",
            "”",
            "v")
        self.assertEqual("eq|eq", self.mapping.map(pos_node, state))


    def test_separable_verb(self):
        """
        Test that a separable verb is mapped as expected.
        """

        # preposition embedded in the node
        pos_node = MockPosNode(
            "WW(vd,vrij,zonder)",
            "schaats_aan",
            "aan_schaatsen",
            "aangeschaatst")
        self.assertEqual("aan$ V|schaats-PASP", self.mapping.map(pos_node))

        # preposition not in node
        pos_node = MockPosNode(
            "WW(inf,vrij,zonder)",
            "wijs_aan",
            "aan_wijzen",
            "wijzen")
        self.assertEqual("V|wijs-INF", self.mapping.map(pos_node))


class MockPosNode:
    """
    Mock representation of a word with an Alpino POS tag.
    """

    def __init__(self, tag, root, lemma, word):
        self.tag = tag
        self.lemma = lemma
        self.root = root
        self.word = word
