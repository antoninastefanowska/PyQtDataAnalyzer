from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt

class DecisionTreeItemModel(QAbstractItemModel):
    def __init__(self, root):
        super().__init__()
        self.root = root

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
                return QAbstractItemModel.createIndex(self, parent.index, 0, parent)
        return QModelIndex()

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=None):
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.DisplayRole:
                return node.label()
        return None