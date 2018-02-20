#!/usr/bin/env python3
"""
Module for reading the parsed sentences and their POS tags.
"""
from lxml import etree

class PosNodesReader:
    """
    Reader used to parse (combined) Alpino XML files.
    """

    def read_sentences(self, file_handle):
        """
        Read the parsed Alpino sentences and give the nodes which are directly
        related to a word in the sentence.

        Returns:
            A generator returning tuples of the form (sentence, PosNode[])
        """
        parsed_xml = etree.parse(
            file_handle, etree.XMLParser(remove_blank_text=True))
        parsed_sentences = parsed_xml.findall(".//alpino_ds")

        if parsed_sentences:
            for sentence in parsed_sentences:
                yield self.read_sentence(sentence)
        elif parsed_xml.find("sentence") is not None:
            # just a single sentence
            yield self.read_sentence(parsed_xml)
        else:
            return

    def read_sentence(self, parsed_sentence):
        """
        Read a sentence structure and return the nodes directly relating to a word.
        """
        sentence = parsed_sentence.find("sentence")
        pos_nodes = parsed_sentence.findall(".//node[@postag]")
        origutt = normalize_utterance(parsed_sentence.find('metadata/meta[@name="origutt"]').get("value"))

        return AlpinoSentence(
            sentence.text,
            sentence.attrib["sentid"],
            sorted((PosNode(node) for node in pos_nodes), key=PosNode.get_sort_key),
            origutt)


class AlpinoSentence:
    """
    Represents a sentence in the grouped Lassy (Alpino) XML file.
    """

    def __init__(self, sentence_text, sentence_id, pos_nodes, origutt):
        self.sentence_text = sentence_text
        self.sentence_id = sentence_id
        self.pos_nodes = pos_nodes
        self.origutt = origutt

class PosNode:
    """
    Represents a word with an Alpino POS tag.
    """

    def __init__(self, pos_node):
        self.begin = int(pos_node.get("begin"))
        self.end = int(pos_node.get("end"))
        self.tag = pos_node.get("postag")
        self.lemma = pos_node.get("lemma")
        self.word = pos_node.get("word")
        self.root = pos_node.get("root")

    def get_sort_key(self):
        """Get a key to sort the nodes by their position in the sentence."""
        return self.begin

def normalize_utterance(text):
    return text.strip()
