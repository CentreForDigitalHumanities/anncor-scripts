"""
Handles the mapping of punctuation symbols to their representations as in the morphological
CHAT tier.
"""
#!/usr/bin/env python3
import csv

class PunctuationMapping:
    """
    Maps the punctuation symbols to their CHAT representations.
    """

    def __init__(self, filename):
        self.__lookup__ = {}
        with open(filename) as csv_file:
            for row in csv.reader(csv_file, delimiter='\t'):
                self.__lookup__[row[0]] = row[1]

    def __getitem__(self, key):
        try:
            self.__lookup__[key]
        except Exception as error:
            raise Exception(f'Unknown punctuation symbol: {key}' ) from error

    def keys(self):
        return self.__lookup__.keys()
