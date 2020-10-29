from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout

class ChartWindow(QMainWindow):
    def __init__(self, parent, chart_canvas):
        super().__init__(parent)
        self.chart_canvas = chart_canvas
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/chartwindow.ui", self)
        chart_layout = self.findChild(QVBoxLayout, "chartLayout")
        chart_layout.addWidget(self.chart_canvas)

    @pyqtSlot()
    def export(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Eksportuj...", "", "Pliki PNG (*.png)", options=QFileDialog.Options())
        if filename:
            self.chart_canvas.save_chart(filename)
