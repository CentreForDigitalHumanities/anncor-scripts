from typing import List

from .types import ParseTree, QueryFunction, ReplaceFunction, Path


class Replacement:
    '''Represents a single replacement.
    A replacement is a combination of search/match queries,
    and a replacing value. It operates on Lassy XML of
    one sentence/utterance.

    Multiple queries can be included. They are combined with AND-logic.

    Multiple replacements can be included. They are executed in order. Each
    replacement function must work in-place (alter the input element).
    '''

    def __init__(self,
                 label: str,
                 queries: List[QueryFunction],
                 replacements: List[ReplaceFunction]):
        self.label = label
        self.queries = queries
        self.replacements = replacements

    def replace(self, path: Path, utterance: ParseTree, dry_run: bool = False):
        if self.__match(utterance):
            for f in self.replacements:
                f(utterance)
            if not dry_run:
                self.__write(path, utterance)
            return True

    def __match(self, utterance: ParseTree):
        gens = (q(utterance) for q in self.queries)
        return all(gens)

    def __write(self, path: Path, utterance: ParseTree):
        with open(path, 'wb') as f:
            # utterance.write(f, pretty_print=True, xml_declaration=True, encoding='UTF-8')
            utterance.write(f, pretty_print=True,
                            doctype='<?xml version="1.0" encoding="UTF-8"?>')
