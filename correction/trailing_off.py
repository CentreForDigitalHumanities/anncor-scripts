from .replacement import Replacement
from .types import ParseTree
from .utils import find_periods, get_sentence


# Query functions
def has_trailing_off(tree: ParseTree) -> bool:
    '''Detects origutt ending in "+..."
    '''
    xpath = '//meta[@name="origutt" and contains(@value, "+...")]'
    return len(tree.xpath(xpath)) == 1

def ends_with_period(tree: ParseTree) -> bool:
    '''Detects sentence ending in "."
    '''
    sentence_text = tree.xpath('//sentence/text()')[0]
    return sentence_text.rstrip().endswith('.')

# Replacement functions
def alter_sentence(tree: ParseTree) -> None:
    '''Strips period from end of sentence
    '''
    elem = get_sentence(tree)
    new_sent = elem.text.rstrip('.').rstrip()
    elem.text = new_sent

def remove_period_node(tree: ParseTree) -> None:
    '''Removes period node
    If multiple period nodes in tree, only remove max(@begin)
    '''
    periods = find_periods(tree)

    if periods:
        last_period = periods[-1]
        last_period.getparent().remove(last_period)

# Replacement object
trail_off = Replacement(label='trailing_off',
                        queries=[has_trailing_off, ends_with_period],
                        replacements=[alter_sentence, remove_period_node])
