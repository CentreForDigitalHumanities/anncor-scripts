#!/usr/bin/env python3
"""
Module for enriching a CHAT file with morphological information.
"""
from .exceptions import NodeMappingException, SentenceMappingException
from .injectable_file import InjectableFile
from .pos_nodes_reader import PosNodesReader


class MorphEnricher:
    """
    Adds morphological information to CHAT files using a provided mapping.
    """

    def __init__(self, pos_mapping):
        self.pos_mapping = pos_mapping
        self.__pos_reader = PosNodesReader()
        self.failed_sentences_count = 0
        self.missing_tags = set()

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
                    try:
                        mapped_sentence = self.__map_sentence(
                            sentence_map[utterance])
                    except SentenceMappingException as exception:
                        mapped_sentence = exception.converted_sentence
                        self.failed_sentences_count += 1
                        for node in exception.pos_nodes:
                            self.missing_tags.add(node.tag)

                    yield "%mor:\t{0}".format(mapped_sentence)
        finally:
            chat_file.close()

    @property
    def has_failures(self):
        """
        Get whether any of the sentences couldn't be converted because a mapping was missing.
        """
        return self.failed_sentences_count > 0

    def __map_nodes(self, nodes, unmapped_nodes):
        for node in nodes:
            try:
                yield self.pos_mapping.map(node)
            except NodeMappingException as exception:
                unmapped_nodes.append(exception.pos_node)
                yield "???|{0}-{1}".format(node.word, node.tag)

    def __map_sentence(self, sentence):
        unmapped_nodes = []

        # expected to be in the right order
        result = " ".join(self.__map_nodes(sentence.pos_nodes, unmapped_nodes))

        if unmapped_nodes:
            raise SentenceMappingException(unmapped_nodes, result)
        else:
            return result
