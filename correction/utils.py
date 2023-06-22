from typing import List, Tuple

from .types import Element, ParseTree, Path
from glob import glob

from lxml import etree

def get_sentence(tree: ParseTree) -> Element:
    elem = tree.xpath('//sentence')[0]
    return elem

def find_periods(tree: ParseTree) -> List[Element]:
    period_xpath = '//node[@pos="punct" and @word="."]'
    return tree.xpath(period_xpath)

def collect_xml_files(in_dir: Path) -> List[Path]:
    return glob(f'{in_dir}/**/*.xml', recursive=True)

def parse_xml_files(files: List[Path]) -> List[Tuple[Path, ParseTree]]:
    return [
        (f, etree.parse(f)) for f in files
    ]
