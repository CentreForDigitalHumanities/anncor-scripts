import unittest
from ..tree import Tree
from ..convert import *

test_file = "conversion/tests/files/s1.xml"

class TestConvert(unittest.TestCase):

    def test_to_tree(self):
        tree = toTree(test_file)
        print(tree)
