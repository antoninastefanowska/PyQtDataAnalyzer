from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QCheckBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

from preprocessing.columnprocessor import ColumnProcessor

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
            processor = ColumnProcessor(column)
            column = processor.discretize(bar_number)

        labels = column.unique()
        values = []

        if not any(isinstance(label, str) for label in labels):
            width = (labels.max() - labels.min()) / len(labels)
        else:
            width = 0.8

        for label in labels:
            values.append(len(column[column == label]))

        self.chart.bar(labels, values, width=width)
        self.chart.set_title(column_name)

    @pyqtSlot()
    def accept(self):
        self.generate_histogram()
        super().accept()
