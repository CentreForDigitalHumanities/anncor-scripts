#!/usr/bin/env python3
"""
Command line interface for adding morphological information to CHAT files.
"""

import sys
import argparse
import logging
import coloredlogs
import os

from conversion import morph_enricher
from conversion import pos_mapping
from conversion import punctuation_mapping

DEFAULT_POS_MAPPING = "conversion/data/pos_mapping.csv"
DEFAULT_PUNCTUATION_MAPPING = "conversion/data/punctuation_mapping.csv"


def main(argv):
    """
    Main entry point.
    """

    coloredlogs.install()

    try:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            "-c", "--chat",
            dest="chat_filenames",
            help="The CHAT file(s) to enrich.",
            metavar="FILE",
            required=True,
            nargs='*')
        parser.add_argument(
            "-p", "--pos",
            dest="pos_filename",
            help="The Treebank LASSY/Alpino XML file containing the POS information.",
            metavar="FILE",
            required=True)
        parser.add_argument(
            "-u", "--punctuation",
            dest="punctuation_filename",
            help="The file containing the punctuation mapping.")
        parser.add_argument(
            "-m", "--mapping",
            dest="mapping_filename",
            help="The mapping file to use.",
            metavar="FILE")
        parser.add_argument(
            "-o", "--output",
            dest="output_directory",
            help="The output_directory to use.",
            metavar="DIRECTORY")

        parser.set_defaults(
            mapping_filename=DEFAULT_POS_MAPPING,
            punctuation_filename=DEFAULT_PUNCTUATION_MAPPING)

        options = parser.parse_args(argv)

        for chat_file in options.chat_filenames:
            if options.output_directory:
                filename = os.path.basename(chat_file)
                writer = FileWriter(options.output_directory, filename)
            else:
                writer = ConsoleWriter()

            try:
                perform_map(options.mapping_filename,
                            options.punctuation_filename,
                            chat_file,
                            options.pos_filename,
                            writer)
            except Exception as exception:
                sys.stderr.write(chat_file)
                raise exception
    except Exception as exception:
        sys.stderr.write(repr(exception) + "\n")
        sys.stderr.write("for help use --help\n\n")
        raise exception


def perform_map(mapping_filename, punctuation_filename, chat_filename, pos_filename, writer):
    """
    Perform the mapping and output to console.
    """

    mapping = pos_mapping.PosMapping(
        punctuation_mapping.PunctuationMapping(punctuation_filename))
    mapping.read(mapping_filename)

    enricher = morph_enricher.MorphEnricher(mapping)
    for line in enricher.map(chat_filename, pos_filename):
        writer.writeline(line)

    if enricher.has_failures:
        logging.error("%s sentence(s) have no tag mapping defined!",
                      enricher.failed_sentences_count)
        logging.error("Missing mapping(s):\n%s",
                      "\n".join(sorted(enricher.missing_tags)))

class FileWriter:
    def __init__(self, directory, filename):
        os.makedirs(directory, exist_ok=True)
        self.file = open(os.path.join(directory, filename), mode='w')

    def writeline(self, line):
        self.file.write(line + '\n')

    def close(self):
        self.file.close()

class ConsoleWriter:
    def writeline(self, line):
        print(line)

    def close(self):
        pass

main(sys.argv[1:])
