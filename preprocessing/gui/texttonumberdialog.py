from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QRadioButton
from PyQt5.QtCore import pyqtSlot

from preprocessing.utils.namegenerator import NameGenerator
from preprocessing.columnprocessor import ColumnProcessor

class TextToNumberDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/texttonumberdialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        cluster_column_combobox = self.findChild(QComboBox, "clusterColumnCombobox")
        column_name_combobox.addItems(self.data.columns)
        cluster_column_combobox.addItems(self.data.columns)

    def text_to_number(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        column_name = column_name_combobox.currentText()
        column = self.data[column_name]

        alphabetically_radio_button = self.findChild(QRadioButton, "alphabeticallyRadioButton")
        by_order_radio_button = self.findChild(QRadioButton, "byOrderRadioButton")
        by_cluster_radio_button = self.findChild(QRadioButton, "byClusterRadioButton")

        name = NameGenerator.get_name(self.data.columns, column_name, "_numeryczne")
        processor = ColumnProcessor(column)

        if alphabetically_radio_button.isChecked():
            self.data[name] = processor.text_to_numbers("alphabetically")

        elif by_order_radio_button.isChecked():
            self.data[name] = processor.text_to_numbers("by_order")

        elif by_cluster_radio_button.isChecked():
            cluster_column_combobox = self.findChild(QComboBox, "clusterColumnCombobox")
            cluster_column_name = cluster_column_combobox.currentText()
            cluster_column = self.data[cluster_column_name]
            self.data[name] = processor.text_to_numbers("by_cluster", cluster_column)

    @pyqtSlot()
    def accept(self):
        self.text_to_number()
        super().accept()
