from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel

class TestingResultWindow(QMainWindow):
    def __init__(self, parent, data, result):
        super().__init__(parent)
        self.result = result
        self.count = len(data.index)
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/testingresultwindow.ui", self)
        result_label = self.findChild(QLabel, "resultLabel")
        result_label.setText(str(self.result) + " / " + str(self.count))
