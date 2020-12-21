import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QCheckBox, QRadioButton, QLineEdit
from PyQt5.QtCore import pyqtSlot

class LoadDataDialog(QDialog):
    def __init__(self, parent, filename):
        super().__init__(parent)
        self.filename = filename
        self.data = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/loaddatadialog.ui", self)

    def load_data(self):
        first_row_checkbox = self.findChild(QCheckBox, "firstRowCheckbox")
        regular_radio_button = self.findChild(QRadioButton, "regularRadioButton")

        if first_row_checkbox.isChecked():
            header = "infer"
        else:
            header = None

        if regular_radio_button.isChecked():
            separator_textbox = self.findChild(QLineEdit, "separatorTextbox")
            delimiter = separator_textbox.text()
            delim_whitespace = False
        else:
            delimiter = None
            delim_whitespace = True

        self.data = pd.read_csv(self.filename, delimiter=delimiter, delim_whitespace=delim_whitespace, header=header, comment='#')

        if not first_row_checkbox.isChecked():
            column_number = len(list(self.data))
            rng = range(1, column_number + 1)
            column_names = ['kolumna' + str(i) for i in rng]
            self.data.columns = column_names[:column_number]

        self.data = self.data.applymap(self.remove_commas)

    def remove_commas(self, value):
        if type(value) == str:
            try:
                return float(value.replace(',', '.'))
            except ValueError:
                return value
        else:
            return value

    @pyqtSlot()
    def accept(self):
        self.load_data()
        super().accept()
