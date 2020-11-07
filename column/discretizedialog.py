import math
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

class DiscretizeDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/discretizedialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        bar_number_textbox = self.findChild(QLineEdit, "barNumberTextbox")
        column_name_combobox.addItems(self.data.columns)
        bar_number_textbox.setValidator(QIntValidator())

    def discretize(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        bar_number_textbox = self.findChild(QLineEdit, "barNumberTextbox")

        column_name = column_name_combobox.currentText()
        column = self.data[column_name]
        min = column.min()
        max = column.max()
        bar_number = int(bar_number_textbox.text())
        step = (max - min) / bar_number

        column = column.map(lambda value: int(math.ceil((value - min) / step)))
        column[column == 0] = 1

        name = column_name + "_dyskretne"
        i = 2
        while name in self.data.columns:
            name = column_name + "_dyskretne_" + str(i)
            i += 1
        self.data[name] = column

    @pyqtSlot()
    def accept(self):
        self.discretize()
        super().accept()

