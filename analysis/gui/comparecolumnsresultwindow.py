from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel

class CompareColumnsResultWindow(QMainWindow):
    def __init__(self, parent, column1_name, column2_name, result, result_info):
        super().__init__(parent)
        self.column1_name = column1_name
        self.column2_name = column2_name
        self.result = result
        self.result_info = result_info
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/comparecolumnsresultwindow.ui", self)
        column1_name_label = self.findChild(QLabel, "columnName1Label")
        column2_name_label = self.findChild(QLabel, "columnName2Label")
        result_label = self.findChild(QLabel, "resultLabel")
        result_info_label = self.findChild(QLabel, "resultInfoLabel")

        column1_name_label.setText(self.column1_name)
        column2_name_label.setText(self.column2_name)
        result_label.setText(self.result)
        result_info_label.setText(self.result_info)