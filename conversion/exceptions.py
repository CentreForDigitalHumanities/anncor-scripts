#!/usr/bin/env python3
"""
The expected exceptions which can occur.
"""


class NodeMappingException(Exception):
    """
    Describes a mapping missing for this POS node.
    """

    def __init__(self, pos_node):
        super(NodeMappingException, self).__init__()
        self.pos_node = pos_node

    def __str__(self):
        return "No mapping exists for POS {0}, word: {1}".format(
            self.pos_node.tag, self.pos_node.word)


class SentenceMappingException(Exception):
    """
    Describes one or more mappings missing for the POS node in this sentence.
    """

    def __init__(self, pos_nodes, converted_sentence):
        super(SentenceMappingException, self).__init__()
        self.pos_nodes = pos_nodes
        self.converted_sentence = converted_sentence

class SentenceNotFoundException(Exception):
    """
    Describes that no parsed sentence could be found for this sentence.
    """

    def __init__(self, text):
        super(SentenceNotFoundException, self).__init__()
        self.text = text
