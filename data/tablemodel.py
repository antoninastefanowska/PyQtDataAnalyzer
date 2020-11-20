from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt5.QtGui import QColor

class TableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.green_rows = None
        self.red_rows = None
        self.data = data

    def rowCount(self, parent=None):
        return len(self.data.values)

    def columnCount(self, parent=None):
        return self.data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(str(self.data.values[index.row()][index.column()]))
            elif role == Qt.BackgroundRole:
                if self.red_rows is not None and index.row() in self.red_rows:
                    return QColor('red')
                elif self.green_rows is not None and index.row() in self.green_rows:
                    return QColor('green')
                else:
                    return QColor('white')
        return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data.columns[col]
        else:
            return super().headerData(col, orientation, role)

    def set_data(self, data):
        self.data = data
