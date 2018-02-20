#!/usr/bin/env python3
"""
Module for enriching a CHAT file with morphological information.
"""
from .exceptions import NodeMappingException, SentenceMappingException, SentenceNotFoundException
from .injectable_file import InjectableFile
from .pos_nodes_reader import PosNodesReader, normalize_utterance


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
                if sentence.origutt in sentence_map:
                    current_mapped = " ".join(self.__map_nodes(sentence.pos_nodes, []))
                    existing_mapped = " ".join(self.__map_nodes(sentence_map[sentence.origutt].pos_nodes, []))
                    if current_mapped != existing_mapped:
                        raise Exception('Same sentence mapped differently! "{0}" != "{1}" for "{2}"'.format(
                            current_mapped,
                            existing_mapped,
                            sentence.origutt))
                else:
                    sentence_map[sentence.origutt] = sentence

        chat_file = InjectableFile(chat_filename)
        current_line = None
        try:
            for line in chat_file.read_lines(False):
                if line.startswith("*") or line.startswith('%') or line.startswith('@'):
                    if current_line:
                        yield self.__parse_line(current_line, sentence_map)
                        current_line = None
                    if line.startswith("*"):
                        current_line = line
                elif current_line != None:
                    current_line += ' ' + line

                yield line

            if current_line:
                yield self.__parse_line(current_line, sentence_map)
        finally:
            chat_file.close()

    def __parse_line(self, line, sentence_map):
        try:
            mapped_sentence = self.__map_sentence(
                sentence_map,
                line.split(':', 1)[1])
        except SentenceMappingException as exception:
            mapped_sentence = exception.converted_sentence
            self.failed_sentences_count += 1
            for node in exception.pos_nodes:
                self.missing_tags.add(node.tag)
        except SentenceNotFoundException as exception:
            mapped_sentence = "???"
            self.missing_tags.add(exception.text)
            self.failed_sentences_count += 1

        return "%mor:\t{0}".format(mapped_sentence)

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

    def __map_sentence(self, sentences, origutt):
        unmapped_nodes = []

        try:
            sentence = sentences[normalize_utterance(origutt)]
        except KeyError:
            raise SentenceNotFoundException('Sentence not found for "{0}" ("{1}")'.format(origutt, normalize_utterance(origutt)))

        # expected to be in the right order
        result = " ".join(self.__map_nodes(sentence.pos_nodes, unmapped_nodes))

        if unmapped_nodes:
            raise SentenceMappingException(unmapped_nodes, result)
        else:
            return result
