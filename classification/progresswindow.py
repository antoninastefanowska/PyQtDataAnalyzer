from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QProgressBar

class ProgressWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_bar = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/progresswindow.ui", self)
        self.progress_bar = self.findChild(QProgressBar, "progressBar")

    def update(self, progress):
        self.progress_bar.setValue(progress)

    def finish(self):
        self.progress_bar.setValue(100)
        self.close()
