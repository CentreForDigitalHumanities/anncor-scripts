#!/usr/bin/env python3
"""
Module for enriching a CHAT file with morphological information.
"""

from .injectable_file import InjectableFile
from .pos_nodes_reader import PosNodesReader

class MorphEnricher:
    """
    Adds morphological information to CHAT files using a provided mapping.
    """
    def __init__(self, pos_mapping):
        self.pos_mapping = pos_mapping
        self.__pos_reader = PosNodesReader()

    def map(self, chat_filename, pos_filename):
        """
        Map a single CHAT file using the provided Lassy XML file containing the morphology
        of the utterances.
        """

        sentence_map = {}

        with open(pos_filename) as pos_file:
            for sentence in self.__pos_reader.read_sentences(pos_file):
                # the sentence id should be a positional number
                sentence_map[int(sentence.sentence_id)] = sentence

        chat_file = InjectableFile(chat_filename)
        try:
            utterance = 0
            for line in chat_file.read_lines(False):
                yield line

                if line.startswith("*"):
                    utterance += 1  # utterances are one-based
                    yield "%mor:\t{0}".format(self.__map_sentence(sentence_map[utterance]))
        finally:
            chat_file.close()

    def __map_sentence(self, sentence):
        # expected to be in the right order
        return " ".join(self.pos_mapping.map(node) for node in sentence.pos_nodes)
