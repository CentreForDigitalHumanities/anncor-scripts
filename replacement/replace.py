from lxml import etree
from typing import Dict, List

# type hints
Element = etree._Element
XPath = etree.XPath

REPLACEMENTS = {
    'eh': {
        'search': {'lemma': 'eh', 'word': 'eh'},
        'remove': ['genus', 'getal', 'graad', 'naamval', 'ntype'],
        'edit': {'postag': 'TSW()', 'pt': 'tsw', 'pos': 'tag'}
    },
    'uh': {
        'search': {'lemma': 'eh', 'word': 'uh'},
        'remove': ['genus', 'getal', 'graad', 'naamval', 'ntype'],
        'edit': {'postag': 'TSW()', 'pt': 'tsw', 'pos': 'tag'}
    },
    'xxx': {
        'search': {'word': 'xxx'},
        'keep_only': ['begin', 'end', 'pos', 'root', 'postag', 'pt', 'lemma', 'word', 'sense', 'rel', 'id'],
        'edit': {'pos': 'tag', 'postag': 'SPEC(onverst)', 'pt': 'spec', 'spectype': 'onverst'}
    },
    'yyy': {
        'search': {'word': 'yyy'},
        'keep_only': ['begin', 'end', 'pos', 'root', 'postag', 'pt', 'lemma', 'word', 'sense', 'rel', 'id'],
        'edit': {'pos': 'tag', 'postag': 'SPEC(onverst)', 'pt': 'spec', 'spectype': 'onverst'}
    },
    'NA()': {
        'search': {'postag': 'NA()'},
        'edit': {'postag': 'TSW()', 'pt': 'tsw', 'pos': 'tag'}
    }
}


class Replacement:
    def __init__(self, search, remove, keep_only, edit):
        self.search: Dict = search
        self.remove: List[str] = remove or []
        self.keep_only: List[str] = keep_only or []
        self.edit: Dict = edit or {}
        self.search_query = self.xpath_query()

    def xpath_query(self) -> XPath:
        conditions = ["@{}='{}'".format(k, v)
                      for k, v in self.search.items()]
        conditions_str = ' and '.join(conditions)
        query_str = '//node[{}]'.format(conditions_str)
        return etree.XPath(query_str)

def convert_replacements(replacements: Dict):
    "Convert replacement specifications to a list of Replacement objects"

    #function for a single replacement
    def single_replacement(key):
        #retrieve replacement specifications
        specs = replacements[key]
        search = specs['search']
        get_specs_with_default = lambda key: specs[key] if key in specs else None #avoid key errors
        remove = get_specs_with_default('remove')
        keep_only = get_specs_with_default('keep_only')
        edit = get_specs_with_default('edit')

        #convert
        return Replacement(search, remove, keep_only, edit)
    
    #map to all replacements
    all_replacements = [single_replacement(key) for key in replacements]
    return all_replacements

def replace_in_tree(syntree, replacements: List[Replacement]):
    #get root node
    root = syntree.getroot()

    #go through replacements
    for rep in replacements:
        #find matches for search
        query = rep.search_query
        matches = query(root)

        for match in matches:
            #check and apply changes for each attribute
            for key in match.attrib:
                if rep.edit and key in rep.edit:
                    match.attrib[key] = rep.edit[key]

                elif rep.remove and key in rep.remove:
                    del match.attrib[key]

                elif rep.keep_only and key not in rep.keep_only:
                    del match.attrib[key]