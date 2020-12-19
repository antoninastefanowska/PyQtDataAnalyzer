from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QRadioButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

from sklearn.metrics import silhouette_score

from metrics.metricsfactory import MetricsFactory
from preprocessing.kmeansclustering import KMeansClustering
from preprocessing.utils.namegenerator import NameGenerator

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
        chosen_value_radiobutton = self.findChild(QRadioButton, "chosenValueRadiobutton")

        start_column_name = start_column_name_combobox.currentText()
        end_column_name = end_column_name_combobox.currentText()
        metrics_name = metrics_name_combobox.currentText()
        initialization_method = initialization_method_combobox.currentText()

        data_part = self.data.loc[:, start_column_name:end_column_name]
        metrics = MetricsFactory.get_by_name(metrics_name, data_part)
        metrics.prepare()

        if chosen_value_radiobutton.isChecked():
            k_value_textbox = self.findChild(QLineEdit, "kValueTextbox")
            k_value = int(k_value_textbox.text())
            k_means_clustering = KMeansClustering(data_part, k_value, metrics, initialization_method)
            cluster_column = k_means_clustering.k_means()
        else:
            k_value = 1
            score = None
            while True:
                k_means_clustering = KMeansClustering(data_part, k_value, metrics, initialization_method)
                cluster_column = k_means_clustering.k_means()
                new_score = silhouette_score(data_part, cluster_column, metrics.get_distance)
                if score is not None and new_score < score:
                    break
                score = new_score
                k_value += 1

        name = NameGenerator.get_name(self.data.columns, "klaster", "")
        self.data[name] = cluster_column

    @pyqtSlot()
    def accept(self):
        self.cluster_analysis()
        super().accept()