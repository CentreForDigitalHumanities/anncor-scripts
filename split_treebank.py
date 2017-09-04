#!/usr/bin/env python3
"""
Split a treebank file containing multiple parsed utterances to one file per utterance.
"""

import argparse
import os
import sys


def main(argv):
    """
    Main entry point.
    """

    try:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            "treebank",
            help="The Treebank XML file to split.")
        parser.add_argument(
            "-b", "--base",
            help="The base filename to use.",
            required=False)

        options = parser.parse_args(argv)

        split(options.treebank, options.base)
    except Exception as exception:
        sys.stderr.write(repr(exception) + "\n")
        sys.stderr.write("for help use --help\n\n")
        raise exception


def split(treebank_filename, base_filename):
    if base_filename is None:
        (_, base_filename) = os.path.split(treebank_filename)

    date_map = {}
    with open(treebank_filename, 'r') as treebank_file:
        treebank_file.readline()
        while True:
            file = read_file(treebank_file)
            if file is None:
                break
            if not (file.date in date_map):
                file_number = input(
                    'Give the number of the file {0}: '.format(file.date))
                date_map[file.date] = file_number
            else:
                file_number = date_map[file.date]
            write_file(base_filename, file_number, file)

    print("# mapping used for " + treebank_filename)
    for date,number in date_map.items():
        print(base_filename + number + ' = ' + date)

def read_file(lines):
    """
    Read the lines of a single file and return it in some useable format.
    Stops the reader at the beginning of the next file, assumes the first line is
    the start of the new file.
    """
    line = lines.readline()
    if line is None or line.find("<alpino_ds") < 0:
        return None

    # remove the additional whitespace at the start of the file
    # TODO: document header?
    tab_width = next(i for i, char in enumerate(line) if char != ' ')
    file_lines = [line[tab_width:]]
    date = None
    for line in lines:
        file_lines.append(line[tab_width:])
        if line.find("</alpino_ds>") >= 0:
            break
        elif line.find("<sentence") >= 0:
            sentence_number = int(line[line.find("sentid=\""):].split('"')[1])
        elif line.find("<meta") >= 0 and line.find("name=\"date\"") > 0:
            date = line[line.find("value=\""):].split('"')[1]

    if date == None:
        print(''.join(file_lines))

    return File(file_lines, sentence_number, date)


def write_file(base_filename, file_number, file):
    with open(base_filename + file_number + '_u' + str(file.sentence_number).zfill(11) + '.xml', 'w') as target:
        target.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        target.writelines(file.lines)


class File:
    def __init__(self, lines, sentence_number, date):
        self.lines = lines
        self.sentence_number = sentence_number
        self.date = date


main(sys.argv[1:])
