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
        self.search_query = self.xpath_query(search)

    def xpath_query(self) -> XPath:
        conditions = ["@{}='{}'".format(k, v)
                      for k, v in self.search.items()]
        conditions_str = ' and '.join(conditions)
        query_str = '//node[{}]'.format(conditions_str)
        return etree.XPath(query_str)


def replace_in_file(replacements: List[Replacement],
                    in_path: str,
                    out_path: str
                    ) -> None:
    tree = etree.parse(in_path)
    root = tree.getroot().xpath('alpino_ds')

    # def replace_in_file(replacements: Dict[str, Any],
    #                     filepath: str,
    #                     out_filepath: str) -> None:
    #     with open(filepath, encoding='UTF-8') as f_in:
    #         doc = Soup(f_in.read(), features='xml').alpino_ds
    #         relpath = os.path.relpath(filepath, WORK_DIR)
    #         logging.info(relpath)
    #         for name, op in replacements.items():
    #             nodes = doc.findAll('node', op['search'])
    #             for node in nodes:
    #                 edit_node(node,
    #                           op['remove'] if 'remove' in op.keys() else None,
    #                           op['keep_only'] if 'keep_only' in op.keys() else None,
    #                           op['edit'])
    #             logging.info(f'{name}:{" "*(20-len(name))}{len(nodes)}')
    #         logging.info('-'*len(filepath))
    #         os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
