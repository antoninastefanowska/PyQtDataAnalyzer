import math
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QCheckBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

class HistogramDialog(QDialog):
    def __init__(self, parent, data, chart):
        super().__init__(parent)
        self.data = data
        self.chart = chart
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/histogramdialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        bar_number_textbox = self.findChild(QLineEdit, "barNumberTextbox")
        column_name_combobox.addItems(self.data.columns)
        bar_number_textbox.setValidator(QIntValidator())

    def generate_histogram(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        discretize_checkbox = self.findChild(QCheckBox, "discretizeCheckbox")
        column_name = column_name_combobox.currentText()
        column = self.data[column_name]

        if discretize_checkbox.isChecked():
            bar_number_textbox = self.findChild(QLineEdit, "barNumberTextbox")
            bar_number = int(bar_number_textbox.text())

            min = column.min()
            max = column.max()
            step = (max - min) / bar_number

            column = column.map(lambda value: math.ceil((value - min) / step) * step + min)
            column[column == 0] = min
        else:
            bar_number = len(column.unique())

        self.chart.hist(column, bins=bar_number)
        self.chart.set_title(column_name)

    def accept(self):
        self.generate_histogram()
        super().accept()
