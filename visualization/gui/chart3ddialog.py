from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

class Chart3DDialog(QDialog):
    def __init__(self, parent, data, chart_canvas):
        super().__init__(parent)
        self.data = data
        self.chart_canvas = chart_canvas
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/chart3ddialog.ui", self)
        x_column_name_combobox = self.findChild(QComboBox, "xColumnNameCombobox")
        y_column_name_combobox = self.findChild(QComboBox, "yColumnNameCombobox")
        z_column_name_combobox = self.findChild(QComboBox, "zColumnNameCombobox")
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        x_column_name_combobox.addItems(self.data.columns)
        y_column_name_combobox.addItems(self.data.columns)
        z_column_name_combobox.addItems(self.data.columns)
        class_column_name_combobox.addItems(self.data.columns)

    def generate_chart(self):
        x_column_name_combobox = self.findChild(QComboBox, "xColumnNameCombobox")
        y_column_name_combobox = self.findChild(QComboBox, "yColumnNameCombobox")
        z_column_name_combobox = self.findChild(QComboBox, "zColumnNameCombobox")
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")

        x_column_name = x_column_name_combobox.currentText()
        y_column_name = y_column_name_combobox.currentText()
        z_column_name = z_column_name_combobox.currentText()
        class_column_name = class_column_name_combobox.currentText()

        self.chart_canvas.generate_3d_chart(self.data, class_column_name, x_column_name, y_column_name, z_column_name)

    @pyqtSlot()
    def accept(self):
        self.generate_chart()
        super().accept()
