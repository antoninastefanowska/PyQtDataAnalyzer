import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableView
from PyQt5.QtCore import pyqtSlot

from tablemodel import TableModel
from loaddatadialog import LoadDataDialog
from texttonumberdialog import TextToNumberDialog
from discretizedialog import DiscretizeDialog
from normalizedialog import NormalizeDialog
from scaledialog import ScaleDialog
from highlightdialog import HighlightDialog
from chart2ddialog import Chart2DDialog
from chart3ddialog import Chart3DDialog
from histogramdialog import HistogramDialog

from chartcanvas import ChartCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.data = None
        self.table_model = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/mainwindow.ui", self)

    @pyqtSlot()
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Otwórz...", "", "Wszystkie pliki (*);;Pliki CSV (*.csv);;Pliki tekstowe (*.txt)", options=QFileDialog.Options())
        if filename:
            dialog = LoadDataDialog(self, filename)
            if dialog.exec_():
                table_view = self.findChild(QTableView, "tableView")
                self.data = dialog.data
                self.table_model = TableModel(self.data)
                table_view.setModel(self.table_model)

    @pyqtSlot()
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Zapisz jako...", "", "Wszystkie pliki (*);;Pliki CSV (*.csv);;Pliki tekstowe (*.txt)", options=QFileDialog.Options())
        if filename:
            self.data.to_csv(filename, sep=';', header=True, index=False)

    @pyqtSlot()
    def text_to_numbers(self):
        dialog = TextToNumberDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def discretize(self):
        dialog = DiscretizeDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def normalize(self):
        dialog = NormalizeDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def scale(self):
        dialog = ScaleDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def highlight(self):
        dialog = HighlightDialog(self, self.data)
        if dialog.exec_():
            self.table_model.green_rows = dialog.smallest_indexes
            self.table_model.red_rows = dialog.biggest_indexes
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def show_chart2d(self):
        chart_canvas = ChartCanvas()
        chart = chart_canvas.axes
        dialog = Chart2DDialog(self, self.data, chart)
        if dialog.exec_():
            new_window = QMainWindow(self)
            new_window.setWindowTitle("Wykres")
            new_window.setCentralWidget(chart_canvas)
            new_window.show()

    @pyqtSlot()
    def show_chart3d(self):
        chart_canvas = ChartCanvas(projection="3d")
        chart = chart_canvas.axes
        dialog = Chart3DDialog(self, self.data, chart)
        if dialog.exec_():
            new_window = QMainWindow(self)
            new_window.setWindowTitle("Wykres")
            new_window.setCentralWidget(chart_canvas)
            new_window.show()

    @pyqtSlot()
    def show_histogram(self):
        chart_canvas = ChartCanvas()
        chart = chart_canvas.axes
        dialog = HistogramDialog(self, self.data, chart)
        if dialog.exec_():
            new_window = QMainWindow(self)
            new_window.setWindowTitle("Wykres")
            new_window.setCentralWidget(chart_canvas)
            new_window.show()

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
