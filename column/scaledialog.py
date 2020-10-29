from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator

class ScaleDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/scaledialog.ui", self)
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        from_textbox = self.findChild(QLineEdit, "fromTextbox")
        to_textbox = self.findChild(QLineEdit, "toTextbox")
        column_name_combobox.addItems(self.data.columns)
        from_textbox.setValidator(QDoubleValidator())
        to_textbox.setValidator(QDoubleValidator())

    def scale(self):
        column_name_combobox = self.findChild(QComboBox, "columnNameCombobox")
        from_textbox = self.findChild(QLineEdit, "fromTextbox")
        to_textbox = self.findChild(QLineEdit, "toTextbox")

        column_name = column_name_combobox.currentText()
        column = self.data[column_name]
        a = float(from_textbox.text())
        b = float(to_textbox.text())
        min = column.min()
        max = column.max()

        name = column_name + "_skalowane"
        i = 2
        while name in self.data.columns:
            name = column_name + "_skalowane_" + str(i)
            i += 1
        self.data[name] = column.map(lambda value: round((b - a) * (value - min) / (max - min) + a, 4))

    @pyqtSlot()
    def accept(self):
        self.scale()
        super().accept()
