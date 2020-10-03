from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

class HighlightDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.smallest_indexes = None
        self.biggest_indexes = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/highlightdialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        smallest_textbox = self.findChild(QLineEdit, "smallestTextbox")
        biggest_textbox = self.findChild(QLineEdit, "biggestTextbox")
        column_name_combobox.addItems(self.data.columns)
        smallest_textbox.setValidator(QIntValidator(0, 100))
        biggest_textbox.setValidator(QIntValidator(0, 100))

    def calculate_indexes(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        smallest_textbox = self.findChild(QLineEdit, "smallestTextbox")
        biggest_textbox = self.findChild(QLineEdit, "biggestTextbox")

        column_name = column_name_combobox.currentText()
        column = self.data[column_name]
        smallest_percent = int(smallest_textbox.text())
        biggest_percent = int(biggest_textbox.text())
        count = column.count()
        smallest_number = int(round(smallest_percent / 100 * count))
        biggest_number = int(round(biggest_percent / 100 * count))
        column = column.sort_values()

        self.smallest_indexes = column.index[:smallest_number]
        self.biggest_indexes = column.index[-biggest_number:]

    @pyqtSlot()
    def accept(self):
        self.calculate_indexes()
        super().accept()
