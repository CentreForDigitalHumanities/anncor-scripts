#!/usr/bin/env python3
"""
Module for enriching a CHAT file with morphological information.
"""
import re
from os import listdir
from os.path import isdir, join

from .exceptions import NodeMappingException, SentenceMappingException, SentenceNotFoundException
from .injectable_file import InjectableFile
from .pos_nodes_reader import PosNodesReader, normalize_utterance

session_pattern = re.compile(r"(^.*[/\\]|\.cha$)", flags=re.IGNORECASE)

class MorphEnricher:
    """
    Adds morphological information to CHAT files using a provided mapping.
    """

    def __init__(self, pos_mapping):
        self.pos_mapping = pos_mapping
        self.__pos_reader = PosNodesReader()
        self.failed_sentences_count = 0
        self.missing_tags = set()
        self.sentence_map = {}

    def read_pos_directories(self, filepath):
        directories = listdir(filepath)
        self.directory_count = len(directories)
        for directory_i in range(0, self.directory_count):
            directory = directories[directory_i]
            dirpath = join(filepath, directory)
            if isdir(dirpath):
                session = session_pattern.sub("", directory)
                files = listdir(dirpath)
                self.file_count = len(files)
                for file_i in range(0, self.file_count):
                    filename = files[file_i]
                    xmlpath = join(dirpath, filename)
                    try:
                        for sentence_i in self.read_pos_file(xmlpath, session):
                            yield (directory_i, file_i, sentence_i)
                    except:
                        raise Exception('Problem parsing ' + xmlpath)

    def read_pos_file(self, filename, session = None):
        with open(filename) as pos_file:
            sentences = list(self.__pos_reader.read_sentences(pos_file))
            self.sentence_count = len(sentences)
            for i in range(0, self.sentence_count):
                sentence = sentences[i]
                if session == None:
                    session = sentence.session
                if not session in self.sentence_map:
                    self.sentence_map[session] = {}
                elif sentence.uttid in self.sentence_map[session]:
                    raise Exception('Duplicate uttid {0} in "{1}! ({2})"'.format(
                        sentence.uttid,
                        session,
                        sentence.sentence_text))

                self.sentence_map[session][sentence.uttid] = sentence

                yield i


    def map(self, chat_filename, replace_existing_mor = True):
        """
        Map a single CHAT file using the provided Lassy XML file containing the morphology
        of the utterances.
        """

        chat_file = InjectableFile(chat_filename)
        session = session_pattern.sub("", chat_filename)
        current_line = None
        uttid = 0
        skipping_mor_lines = False
        try:
            for line in chat_file.read_lines(False):
                if line.startswith("*") or line.startswith('%') or line.startswith('@'):
                    if replace_existing_mor:
                        skipping_mor_lines = line.startswith('%mor')
                    if current_line:
                        yield self.__parse_line(current_line, self.sentence_map, session, uttid)
                        uttid += 1
                        current_line = None
                    if line.startswith("*"):
                        current_line = line
                    else:
                        current_line = None
                elif current_line != None:
                    current_line += ' ' + line
                if not skipping_mor_lines:
                    yield line

            if current_line:
                yield self.__parse_line(current_line, sentence_map, session, uttid)
        finally:
            chat_file.close()

    def __parse_line(self, line, sentence_map, session, uttid):
        try:
            mapped_sentence = self.__map_sentence(
                sentence_map,
                session,
                uttid)
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
        state = {}
        for i, node in enumerate(nodes):
            try:
                yield self.pos_mapping.map(node, state, i == len(nodes) - 1)
            except NodeMappingException as exception:
                unmapped_nodes.append(exception.pos_node)
                yield "???|{0}-{1}".format(node.word, node.tag)

    def __map_sentence(self, sentences, session, uttid):
        unmapped_nodes = []

        try:
            sentence = sentences[session][uttid]
        except KeyError:
            try:
                sentence = sentences[None][uttid]
            except KeyError:
                raise SentenceNotFoundException('Sentence not found for "{0}" ({1})'.format(session, uttid))

        # expected to be in the right order
        result = " ".join(self.__map_nodes(sentence.pos_nodes, unmapped_nodes))

        if unmapped_nodes:
            raise SentenceMappingException(unmapped_nodes, result)
        else:
            return result
