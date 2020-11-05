from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

class NormalizeAllDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/classcolumndialog.ui", self)
        class_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        class_name_combobox.addItems(self.data.columns)

    def normalize(self):
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        class_column_name = class_column_name_combobox.currentText()
        column_names = self.data.columns[self.data.columns != class_column_name]

        for column_name in column_names:
            column = self.data[column_name]
            mean = column.mean()
            std = column.std()
            self.data[column_name] = column.map(lambda value: round((value - mean) / std, 4))

    @pyqtSlot()
    def accept(self):
        self.normalize()
        super().accept()
