from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

from .namegenerator import NameGenerator
from .columnprocessor import ColumnProcessor

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

        processor = ColumnProcessor(column)
        name = NameGenerator.get_name(self.data.columns, column_name, "_normalizowane")
        self.data[name] = processor.normalize()

    @pyqtSlot()
    def accept(self):
        self.normalize()
        super().accept()
