from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QRadioButton
from PyQt5.QtCore import pyqtSlot

from .namegenerator import NameGenerator
from .columnprocessor import ColumnProcessor

class TextToNumberDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/texttonumberdialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        column_name_combobox.addItems(self.data.columns)

    def text_to_number(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        column_name = column_name_combobox.currentText()
        column = self.data[column_name]

        alphabetically_radio_button = self.findChild(QRadioButton, "alphabeticallyRadioButton")
        alphabetically = alphabetically_radio_button.isChecked()

        processor = ColumnProcessor(column)
        name = NameGenerator.get_name(self.data.columns, column_name, "_numeryczne")
        self.data[name] = processor.text_to_numbers(alphabetically)

    @pyqtSlot()
    def accept(self):
        self.text_to_number()
        super().accept()
