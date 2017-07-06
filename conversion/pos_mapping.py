#!/usr/bin/env python3
"""
Handles the mapping of a POS Lassy XML node to the format used in CHAT.
"""
import csv
from enum import Enum
from .exceptions import NodeMappingException


class WordForm(Enum):
    """
    Different word forms to be used for formatting.
    """

    LEMMA = "lemma"
    ROOT = "root"


class PosMapping:
    """
    Mapping of POS nodes to Lassy XML format. Use read() to initialize the mapping.
    """

    def __init__(self, punctuation_mapping):
        self.lookup = {}
        self.punctuation_mapping = punctuation_mapping

    def __getitem__(self, key):
        return self.lookup[key]

    def read(self, filename):
        """
        Read the mapping file, expecting a semicolon separated file containing 4 columns:
         * Lassy POS tag
         * CHAT POS tag
         * Word form to use
         * Affix (optional)
        """
        self.lookup = {}

        with open(filename) as csv_file:
            for row in csv.reader(csv_file, delimiter=';'):
                if row[3] == "":
                    postfix = None
                else:
                    postfix = row[3]

                self.lookup[row[0]] = (row[1], WordForm(row[2]), postfix)

    def map(self, pos_node):
        """
        Map a POS Lassy node to a morphological tag as used in CHAT.

        Returns:
            The string to use in the MOR tier.

        Raises:
            PosMappingException: A mapping is missing.
        """

        mapping = self.lookup.get(pos_node.tag)
        if mapping:
            (pos_tag, word_form_type, affix) = mapping
            if word_form_type == WordForm.LEMMA:
                stem = pos_node.lemma
            elif word_form_type == WordForm.ROOT:
                stem = pos_node.root
            else:
                raise Exception(
                    "Unknown word form type: {0}".format(word_form_type))

            if pos_tag == "V" and '_' in pos_node.root:
                # Separable verbs should mark the preposition separately.
                [verb, preposition] = pos_node.root.split('_')
                if pos_node.word.startswith(preposition):
                    return "{0}$ {1}".format(preposition, self.__format_stem(pos_tag, verb, affix))
                else:
                    return self.__format_stem(pos_tag, verb, affix)
            elif pos_tag == "PUNCT":
                return self.__format_stem(pos_tag, self.punctuation_mapping[stem])
            else:
                return self.__format_stem(pos_tag, stem, affix)
        else:
            raise NodeMappingException(pos_node)

    def __format_stem(self, pos_tag, stem, affix=None):
        if affix is None:
            return "{0}|{1}".format(pos_tag, stem)
        else:
            return "{0}|{1}{2}".format(pos_tag, stem, affix)
