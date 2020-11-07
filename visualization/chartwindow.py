from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout

class ChartWindow(QMainWindow):
    def __init__(self, parent, chart_canvas, vectors=None, xlims=None, ylims=None):
        super().__init__(parent)
        self.chart_canvas = chart_canvas
        self.vectors = vectors
        self.xlims = xlims
        self.ylims = ylims
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

    @pyqtSlot()
    def keyPressEvent(self, event):
        if self.vectors != None and len(self.vectors) > 0:
            if event.key() == QtCore.Qt.Key_Space:
                vector = self.vectors.pop(0)
                self.draw_vector(vector)
            elif event.key() == QtCore.Qt.Key_Return:
                for vector in self.vectors:
                    self.draw_vector(vector)

    def draw_vector(self, vector):
        chart = self.chart_canvas.get_subplot(0)
        color = 'green' if vector.orientation == 1 else 'red'
        if vector.column_name == chart.get_xlabel():
            chart.plot([vector.point, vector.point], [self.ylims[0], self.ylims[1]], "k-", lw=1, label="_not in legend", color=color)
        elif vector.column_name == chart.get_ylabel():
            chart.plot([self.xlims[0], self.xlims[1]], [vector.point, vector.point], "k-", lw=1, label="_not in legend", color=color)
        self.chart_canvas.draw()
