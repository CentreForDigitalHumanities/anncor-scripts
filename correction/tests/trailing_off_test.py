from lxml import etree

from ..trailing_off import (alter_sentence, ends_with_period, has_trailing_off,
                            remove_period_node)
from ..utils import find_periods, get_sentence


def test_queries(example):
    assert has_trailing_off(example)
    assert ends_with_period(example)

def test_replacements(example):
    # Before
    assert get_sentence(example).text == 'eh jij ook e xxx pulle .'
    assert len(find_periods(example)) == 1

    # Run replacements
    assert alter_sentence(example) is None
    assert remove_period_node(example) is None

    # After
    assert get_sentence(example).text == 'eh jij ook e xxx pulle'
    print(etree.tostring(example, pretty_print=True))
    assert len(find_periods(example)) == 0
