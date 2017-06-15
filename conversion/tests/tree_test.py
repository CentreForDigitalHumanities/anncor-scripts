import unittest
from ..tree import Tree

test_file = "tests/files/s1.xml"

class TestTree(unittest.TestCase):
    def setUp(self):
        self.tree = Tree("Root")
        self.child1 = Tree("child1")
        self.child2 = Tree("child2")
        self.child2a = Tree("child2a")
        self.tree.add_children([self.child1, self.child2])
        self.child2.add_child(self.child2a)

    def test_has(self):
        self.assertTrue(self.tree.has(self.child2a))
        self.assertTrue(self.tree.has(self.child1))
        child3 = Tree("child3")
        self.assertFalse(self.tree.has(child3))
        self.assertTrue(self.tree.has(Tree("child1")))

    def test_get(self):
        self.assertEqual(self.tree.get("child1"),self.child1)
        self.assertEqual(self.tree.get("child2a"), self.child2a)
        self.assertEqual(self.tree.get("Root"), self.tree)

    def test_insert(self):
        newTree = Tree("child2")
        child2b = Tree("child2b")
        child2c = Tree("child2c")
        newTree.add_children([child2b, child2c])
        self.tree.insert(newTree)
        self.assertEqual(self.child2.children, [self.child2a, child2b, child2c])
