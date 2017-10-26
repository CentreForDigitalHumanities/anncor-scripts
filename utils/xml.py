"""
Contains functions to manipulate xml files
"""
from lxml import etree
import difflib
count = 0
def compare_xml_tag(file_1_ref, file_2_ref, tag, ignore_characters = []):
    """
    Compares the tag of both files, will only look at the first instance of the tag
    :param file_1_ref:
    :param file_2_ref:
    :param tag1: tag to look up in the first file
    :param tag2: tag to look up in the second file
    :return: the first difference it finds
    """
    print("start comparing")
    tree_1 = etree.parse(file_1_ref)
    tree_2 = etree.parse(file_2_ref)
    text_1 = tree_1.xpath("//{}".format(tag))[0].text
    text_2 = tree_2.xpath("//{}".format(tag))[0].text

    return compare_text(text_1, text_2, ignore_characters)

def compare_two_xml_tag(file_1_ref, file_2_ref, tag1, tag2, ignore_characters=[]):
    tree_1 = etree.parse(file_1_ref)
    tree_2 = etree.parse(file_2_ref)
    text_1 = tree_1.xpath("//{}".format(tag1))[0].text
    text_2 = tree_2.xpath("//{}".format(tag2))[0].text
    result = compare_text(text_1, text_2, ignore_characters)
    return result


def trim_text(text, ignore_characters=[]):
    new_text = text
    for ch in ignore_characters:

        new_text = new_text.replace(ch, "")
    return new_text



def compare_text(text_1, text_2, ignore_characters=[]):
    """
    Compare the texts and returns characters that differ.Ignores the given character (if it is found then it will go to
    the next character)
    :param text_1:
    :param text_2:
    :return:
    """
    print("compare text")
    print(text_1)
    print(text_2)
    results = []
    new_text_1 = trim_text(text_1, ignore_characters)
    new_text_2 = trim_text(text_2, ignore_characters)
    if new_text_1 == new_text_2:
        return []
    else:
        return [(text_1, text_2)]
