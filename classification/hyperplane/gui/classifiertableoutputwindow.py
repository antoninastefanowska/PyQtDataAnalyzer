from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableView, QFileDialog
from PyQt5.QtCore import pyqtSlot

from data.tablemodel import TableModel

class ClassifierTableOutputWindow(QMainWindow):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.table_model = TableModel(data)
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/classifiertableoutputwindow.ui", self)
        table_view = self.findChild(QTableView, "tableView")
        table_view.setModel(self.table_model)

    @pyqtSlot()
    def export(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Zapisz jako...", "", "Wszystkie pliki (*);;Pliki CSV (*.csv);;Pliki tekstowe (*.txt)", options=QFileDialog.Options())
        if filename:
            self.data.to_csv(filename, sep=';', header=True, index=False)