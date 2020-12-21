class TreeNode:
    def __init__(self, column_name=None, test_value=None, class_value=None):
        self.children = []
        self.column_name = column_name
        self.test_value = test_value
        self.class_value = class_value
        self.parent = None
        self.index = 0

    def add_child(self, child):
        child.parent = self
        child.index = len(self.children)
        self.children.append(child)

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
        else:
            return self.class_value

    def label(self):
        if self.parent:
            s = self.parent.column_name + " = " + str(self.test_value)
            if self.class_value:
                s += " : " + self.class_value
            return s
        else:
            return "ROOT"