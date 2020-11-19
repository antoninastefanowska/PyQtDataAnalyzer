from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

from classification.knn.classifier.metricsfactory import MetricsFactory
from .kmeansclustering import KMeansClustering
from .namegenerator import NameGenerator

class ClusterAnalysisDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/clusteranalysisdialog.ui", self)
        start_column_name_combobox = self.findChild(QComboBox, "startColumnNameCombobox")
        end_column_name_combobox = self.findChild(QComboBox, "endColumnNameCombobox")
        metrics_name_combobox = self.findChild(QComboBox, "metricsNameCombobox")
        k_value_textbox = self.findChild(QLineEdit, "kValueTextbox")

        metrics_name_combobox.addItems(MetricsFactory.NAMES)
        start_column_name_combobox.addItems(self.data.columns)
        end_column_name_combobox.addItems(self.data.columns)
        k_value_textbox.setValidator(QIntValidator())

    def cluster_analysis(self):
        start_column_name_combobox = self.findChild(QComboBox, "startColumnNameCombobox")
        end_column_name_combobox = self.findChild(QComboBox, "endColumnNameCombobox")
        metrics_name_combobox = self.findChild(QComboBox, "metricsNameCombobox")
        initialization_method_combobox = self.findChild(QComboBox, "initializationMethodCombobox")
        k_value_textbox = self.findChild(QLineEdit, "kValueTextbox")

        start_column_name = start_column_name_combobox.currentText()
        end_column_name = end_column_name_combobox.currentText()
        metrics_name = metrics_name_combobox.currentText()
        initialization_method = initialization_method_combobox.currentText()
        k_value = int(k_value_textbox.text())

        data_part = self.data.loc[:, start_column_name:end_column_name]
        metrics = MetricsFactory.get_by_name(metrics_name, data_part)

        k_means_clustering = KMeansClustering(data_part, k_value, metrics, initialization_method)
        cluster_column = k_means_clustering.k_means()
        name = NameGenerator.get_name(self.data.columns, "klaster", "")
        self.data[name] = cluster_column

    @pyqtSlot()
    def accept(self):
        self.cluster_analysis()
        super().accept()