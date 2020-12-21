from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt5.QtWidgets import QAction

from .classifieritemnode import ClassifierItemNode

class ClassifierItemModel(QAbstractItemModel):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.classifiers = []
        self.root = ClassifierItemNode()

    def add_classifier(self, classifier):
        self.classifiers.append(classifier)
        node = ClassifierItemNode(classifier.get_name())

        action = QAction("Wyświetl model")
        action.triggered.connect(lambda: self.context.show_classifier_output(classifier))
        node.add_action(action)
        action = QAction("Klasyfikuj nowy obiekt")
        action.triggered.connect(lambda: self.context.classify_new_object(classifier))
        node.add_action(action)
        action = QAction("Klasyfikuj obiekt z pliku")
        action.triggered.connect(lambda: self.context.classify_loaded_object(classifier))
        node.add_action(action)

        params = classifier.get_param_list()
        for param in params:
            param_node = ClassifierItemNode(param)
            node.add_child(param_node)
        self.root.add_child(node)

    def rowCount(self, parent=None):
        if parent.isValid():
            return parent.internalPointer().child_count()
        return self.root.child_count()

    def index(self, row, column, parent=None):
        if parent.isValid():
            p = parent.internalPointer()
        else:
            p = self.root

        if not QAbstractItemModel.hasIndex(self, row, column, parent):
            return QModelIndex()

        child = p.child(row)
        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QModelIndex()

    def parent(self, index):
        if index.isValid():
            parent = index.internalPointer().parent
            if parent:
                return QAbstractItemModel.createIndex(self, parent.row, 0, parent)
        return QModelIndex()

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=None):
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.DisplayRole:
                return node.label(index.column())
        return None