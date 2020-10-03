from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

class NormalizeDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/normalizedialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        column_name_combobox.addItems(self.data.columns)

    def normalize(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        column_name = column_name_combobox.currentText()
        column = self.data[column_name]
        mean = column.mean()
        std = column.std()

        self.data[column_name + "_normalizowane"] = column.map(lambda value: round((value - mean) / std, 2))

    @pyqtSlot()
    def accept(self):
        self.normalize()
        super().accept()
