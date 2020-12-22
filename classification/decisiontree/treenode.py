class TreeNode:
    def __init__(self, column_name=None, test_value=None, class_value=None, node_size=0):
        self.children = []
        self.column_name = column_name
        self.test_value = test_value
        self.class_value = class_value
        self.parent = None
        self.index = 0
        self.node_size = node_size

    def parent_size(self):
        return self.parent.node_size if self.parent else self.node_size

    def is_leaf(self):
        return not self.children

    def add_child(self, child):
        child.parent = self
        child.index = len(self.children)
        self.children.append(child)

    def turn_to_leaf(self, class_value):
        for child in self.children:
            child.parent = None
            child.index = 0
        self.children.clear()
        self.class_value = class_value

    def child_count(self):
        return len(self.children)

    def child(self, index):
        return self.children[index]

    def is_true(self, data_object):
        return data_object[self.parent.column_name] == self.test_value

    def get_class(self, data_object):
        if self.children:
            for child in self.children:
                if child.is_true(data_object):
                    return child.get_class(data_object)
        return self.class_value

    def label(self):
        if self.parent:
            s = self.parent.column_name + " = " + str(self.test_value)
            if self.is_leaf():
                s += " : " + self.class_value
            s += " (" + str(self.node_size) + "/" + str(self.parent_size()) + ")"
            return s
        else:
            return "ROOT"