from PyQt5.QtWidgets import QMenu

class ClassifierItemNode:
    def __init__(self, data=None):
        self.children = []
        self.data = data
        self.parent = None
        self.menu = None
        self.actions = None
        self.row = 0

        if type(data) is str:
            self.data = [data]
        else:
            self.data = data

    def label(self, column):
        if 0 <= column < len(self.data):
            return self.data[column]

    def column_count(self):
        return len(self.data)

    def child_count(self):
        return len(self.children)

    def child(self, row):
        if row >= 0 and row < len(self.children):
            return self.children[row]

    def parent(self):
        return self.parent

    def add_child(self, child):
        child.parent = self
        child.row = len(self.children)
        self.children.append(child)

    def add_action(self, action):
        if self.actions is None:
            self.actions = []
        if self.menu is None:
            self.menu = QMenu()
        self.actions.append(action)
        self.menu.addAction(action)