from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

from .classifier.metricsfactory import MetricsFactory

class KNNClassifierDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.class_column_name = None
        self.metrics = None
        self.k_value = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/knnclassifierdialog.ui", self)
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        metrics_name_combobox = self.findChild(QComboBox, "metricsNameCombobox")
        k_value_textbox = self.findChild(QLineEdit, "kValueTextbox")

        metrics_name_combobox.addItems(MetricsFactory.NAMES)
        class_column_name_combobox.addItems(self.data.columns)
        k_value_textbox.setValidator(QIntValidator())

    def save_options(self):
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        metrics_name_combobox = self.findChild(QComboBox, "metricsNameCombobox")
        k_value_textbox = self.findChild(QLineEdit, "kValueTextbox")

        self.class_column_name = class_column_name_combobox.currentText()
        self.k_value = int(k_value_textbox.text())
        metrics_name = metrics_name_combobox.currentText()

        no_class_data = self.data.drop(self.class_column_name, axis=1)
        self.metrics = MetricsFactory.get_by_name(metrics_name, no_class_data)

    @pyqtSlot()
    def accept(self):
        self.save_options()
        super().accept()
