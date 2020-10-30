from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

class ClassColumnDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.class_column_name = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/classcolumndialog.ui", self)
        class_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        class_name_combobox.addItems(self.data.columns)

    @pyqtSlot()
    def accept(self):
        class_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        self.class_column_name = class_name_combobox.currentText()
        super().accept()
