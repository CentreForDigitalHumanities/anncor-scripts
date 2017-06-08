from lxml import etree
from .tree import Tree

#http://effbot.org/zone/element.htm
def iterparent(tree, tag):
    for parent in tree.getiterator(tag):
        for child in parent:
            yield parent, child

def iterparentchildrelations(tree, tag):
    for parent in tree.getiterator(tag):
        children = []
        for child in parent:
            children.append(child)
        yield parent, children


def toTree(file_ref):
    file_tree = etree.parse(file_ref)
    tree = Tree("root")
    for parent, children in iterparentchildrelations(file_tree, "node"):
        parent_tree = Tree(parent)
        for child in children:
            parent_tree.addChild(Tree(child))
        tree.insert(parent_tree)
    return tree







