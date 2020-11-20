from matplotlib.patches import Patch
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtCore import pyqtSlot

from visualization.utils.colorgenerator import ColorGenerator

class Chart2DDialog(QDialog):
    def __init__(self, parent, data, chart):
        super().__init__(parent)
        self.data = data
        self.chart = chart
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

        class_column = self.data[self.class_column_name]
        classes = class_column.unique()
        class_dictionary = {}
        for value in classes:
            data_part = self.data[class_column == value]
            class_dictionary[value] = (data_part[self.x_column_name], data_part[self.y_column_name])

        patches = []
        i = 0
        classes.sort()
        for class_key in classes:
            color = ColorGenerator.get_color(i)
            self.chart.scatter(class_dictionary[class_key][0], class_dictionary[class_key][1], c=color)
            patches.append(Patch(color=color, label=class_key))
            i += 1

        self.chart.set_xlabel(self.x_column_name)
        self.chart.set_ylabel(self.y_column_name)
        self.chart.legend(handles=patches)

    @pyqtSlot()
    def accept(self):
        self.generate_chart()
        super().accept()
