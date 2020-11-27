from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

from ..columnanalyzer import ColumnAnalyzer
from ..similarity.similarityfactory import SimilarityFactory

class CompareColumnsDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.column1_name = None
        self.column2_name = None
        self.result = None
        self.similarity_metrics_name = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/comparecolumnsdialog.ui", self)
        column1_name_combobox = self.findChild(QComboBox, "columnName1Combobox")
        column2_name_combobox = self.findChild(QComboBox, "columnName2Combobox")
        similarity_metrics_combobox = self.findChild(QComboBox, "similarityMetricsCombobox")
        column1_name_combobox.addItems(self.data.columns)
        column2_name_combobox.addItems(self.data.columns)
        similarity_metrics_combobox.addItems(SimilarityFactory.NAMES)

    def compare_columns(self):
        column1_name_combobox = self.findChild(QComboBox, "columnName1Combobox")
        column2_name_combobox = self.findChild(QComboBox, "columnName2Combobox")
        similarity_metrics_combobox = self.findChild(QComboBox, "similarityMetricsCombobox")

        self.column1_name = column1_name_combobox.currentText()
        self.column2_name = column2_name_combobox.currentText()
        self.similarity_metrics_name = similarity_metrics_combobox.currentText()

        column1 = self.data[self.column1_name]
        column2 = self.data[self.column2_name]
        similarity_metrics = SimilarityFactory.get_by_name(self.similarity_metrics_name)

        analyzer = ColumnAnalyzer(column1)
        self.result = str(round(analyzer.compare(column2, similarity_metrics), 4))

    @pyqtSlot()
    def accept(self):
        self.compare_columns()
        super().accept()