from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

class Chart2DDialog(QDialog):
    def __init__(self, parent, data, chart_canvas):
        super().__init__(parent)
        self.data = data
        self.chart_canvas = chart_canvas
        self.x_column_name = None
        self.y_column_name = None
        self.class_column_name = None
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/chart2ddialog.ui", self)
        x_column_name_combobox = self.findChild(QComboBox, "xColumnNameCombobox")
        y_column_name_combobox = self.findChild(QComboBox, "yColumnNameCombobox")
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")
        x_column_name_combobox.addItems(self.data.columns)
        y_column_name_combobox.addItems(self.data.columns)
        class_column_name_combobox.addItems(self.data.columns)

    def generate_chart(self):
        x_column_name_combobox = self.findChild(QComboBox, "xColumnNameCombobox")
        y_column_name_combobox = self.findChild(QComboBox, "yColumnNameCombobox")
        class_column_name_combobox = self.findChild(QComboBox, "classColumnNameCombobox")

        self.x_column_name = x_column_name_combobox.currentText()
        self.y_column_name = y_column_name_combobox.currentText()
        self.class_column_name = class_column_name_combobox.currentText()

        self.chart_canvas.generate_2d_chart(self.data, self.class_column_name, self.x_column_name, self.y_column_name)

    @pyqtSlot()
    def accept(self):
        self.generate_chart()
        super().accept()
