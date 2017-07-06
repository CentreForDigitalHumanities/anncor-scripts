import unittest
from ..tree import Tree
from ..convert import *

TEST_FILE = "conversion/tests/files/s1.xml"

class TestConvert(unittest.TestCase):
    def test_to_tree(self):
        tree = to_tree(TEST_FILE)
        print(tree)
