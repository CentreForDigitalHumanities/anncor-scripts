from lxml import etree
from .tree import Tree

#http://effbot.org/zone/element.htm
def iter_parent(tree, tag):
    for parent in tree.getiterator(tag):
        for child in parent:
            yield parent, child

def iter_parent_child_relations(tree, tag):
    for parent in tree.getiterator(tag):
        children = []
        for child in parent:
            children.append(child)
        yield parent, children


def to_tree(file_ref):
    file_tree = etree.parse(file_ref)
    tree = Tree("root")
    for parent, children in iter_parent_child_relations(file_tree, "node"):
        parent_tree = Tree(parent)
        for child in children:
            parent_tree.add_child(Tree(child))
        tree.insert(parent_tree)
    return tree






