class Tree:
    def __init__(self, root):
        self.root = root
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children += children

    def insert(self, tree):
        """
        Adds a sub-tree to this tree, if this tree already has a given root node, it combines
        the children of the root node.
        """
        child = self.get(tree.root)
        parent = child if child else self
        parent.add_children(tree.children)

    def has(self, child):
        if child.root == self.root:
            return True

        for next_child in self.children:
            if next_child.has(child):
                return True

        return False

    def get(self, root):
        if root == self.root:
            return self
        for next_child in self.children:
            child = next_child.get(root)
            if child:
                return child
        return None

    def __str__(self):
        children_str = ""
        for child in self.children:
            children_str += str(child.root)
        for child in self.children:
            pass
        begin = '{} \n {} '.format(self.root, children_str)
        return begin
