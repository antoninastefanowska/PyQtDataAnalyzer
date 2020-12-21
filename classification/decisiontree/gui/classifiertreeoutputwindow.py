from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTreeView

from classification.decisiontree.utils.decisiontreeitemmodel import DecisionTreeItemModel

class ClassifierTreeOutputWindow(QMainWindow):
    def __init__(self, parent, tree):
        super().__init__(parent)
        self.tree_model = DecisionTreeItemModel(tree)
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/classifiertreeoutputwindow.ui", self)
        tree_view = self.findChild(QTreeView, "treeView")
        tree_view.setModel(self.tree_model)