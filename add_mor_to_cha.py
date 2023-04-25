#!/usr/bin/env python3
"""
Command line interface for adding morphological information to CHAT files.
"""

import sys
import argparse
import logging
import coloredlogs
import os

from tqdm import tqdm

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
            dest="pos_filepath",
            help="The Treebank LASSY/Alpino XML file or directory containing the POS information.",
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
        parser.add_argument(
            "-f",
            "--force",
            dest="force",
            default=False,
            help="Continue on error",
            action='store_true')

        parser.set_defaults(
            mapping_filename=DEFAULT_POS_MAPPING,
            punctuation_filename=DEFAULT_PUNCTUATION_MAPPING)

        options = parser.parse_args(argv)
        write_files = True if options.output_directory else False
        enricher = prepare_map(options.mapping_filename,
                               options.punctuation_filename,
                               options.pos_filepath,
                               write_files)

        for chat_file in options.chat_filenames:
            if write_files:
                filename = os.path.basename(chat_file)
                writer = FileWriter(options.output_directory, filename)
            else:
                writer = ConsoleWriter()
            try:
                perform_map(enricher, chat_file, options.pos_filepath, writer)
            except Exception as exception:
                sys.stderr.write('Problem in file: ' + chat_file + '\n')
                if not options.force:
                    raise exception
    except Exception as exception:
        sys.stderr.write(repr(exception) + "\n")
        sys.stderr.write("for help use --help\n\n")
        raise exception


def prepare_map(mapping_filename, punctuation_filename, pos_filepath, show_progress):
    """
    Prepare the mapping and output to console.
    """

    mapping = pos_mapping.PosMapping(
        punctuation_mapping.PunctuationMapping(punctuation_filename))
    mapping.read(mapping_filename)

    enricher = morph_enricher.MorphEnricher(mapping)

    if os.path.isfile(pos_filepath):
        iterator = enricher.read_pos_file(pos_filepath)
        single_file = True
    else:
        iterator = enricher.read_pos_directories(pos_filepath)
        single_file = False

    if not show_progress:
        enumerate(iterator)
    else:
        with tqdm(iterator, total=1, unit=' sentences', desc=pos_filepath) as progress:
            if single_file:
                for i in iterator:
                    progress.total = enricher.sentence_count
                    progress.update(1)
            else:
                current_directory = -1
                current_file = -1
                directory_file_count = 0
                sentence_count = 0

                total_file_index = 0
                total_file_estimate = 1
                total_sentence_estimate = 1

                for (directory_i, file_i, sentence_i) in iterator:
                    if directory_i != current_directory:
                        current_directory = directory_i
                        directory_file_count += enricher.file_count
                        average = directory_file_count / (directory_i + 1)
                        total_file_estimate = (
                            enricher.directory_count - directory_i) * average

                    if file_i != current_file:
                        sentence_count += enricher.sentence_count
                        current_file = file_i
                        total_file_index += 1
                        average = sentence_count / total_file_index
                        total_sentence_estimate = average * total_file_estimate

                    progress.total = total_sentence_estimate
                    progress.update(1)

        return enricher


def perform_map(enricher, chat_filename, pos_filepath, writer):
    for line in enricher.map(chat_filename, pos_filepath):
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
