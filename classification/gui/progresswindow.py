from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QLabel

class ProgressWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_bar = None
        self.status_label = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/progresswindow.ui", self)
        self.progress_bar = self.findChild(QProgressBar, "progressBar")
        self.status_label = self.findChild(QLabel, "statusLabel")

    def update(self, progress):
        self.progress_bar.setValue(progress)

    def update_status(self, status):
        self.status_label.setText(status)

    def finish(self):
        self.progress_bar.setValue(100)
        self.close()
