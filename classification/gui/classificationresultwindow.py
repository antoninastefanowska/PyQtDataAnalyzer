from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel

class ClassificationResultWindow(QMainWindow):
    def __init__(self, parent, data_object, classifier):
        super().__init__(parent)
        self.data_object = data_object
        self.class_column_name = classifier.class_column_name
        self.classifier = classifier
        self.result = None
        self.result_info = None
        self.classify()
        self.load_ui()

    def classify(self):
        self.result = self.classifier.classify(self.data_object)
        self.result_info = self.classifier.get_result_info_string()

    def load_ui(self):
        uic.loadUi("ui/classificationresultwindow.ui", self)
        column_names_layout = self.findChild(QHBoxLayout, "columnNamesLayout")
        column_values_layout = self.findChild(QHBoxLayout, "columnValuesLayout")
        attributes_layout = self.findChild(QVBoxLayout, "attributesLayout")
        class_column_name_label = self.findChild(QLabel, "classColumnNameLabel")
        result_label = self.findChild(QLabel, "resultLabel")
        result_info_label = self.findChild(QLabel, "resultInfoLabel")

        class_column_name_label.setText(self.class_column_name)
        result_label.setText(str(self.result))
        result_info_label.setText(self.result_info)

        column_names = self.data_object.index
        i = 0
        for column_name in column_names:
            column_name_label = QLabel()
            column_name_label.setAlignment(QtCore.Qt.AlignCenter)
            column_name_label.setText(column_name)
            column_names_layout.addWidget(column_name_label)

            column_value_label = QLabel()
            font = column_value_label.font()
            font.setBold(True)
            column_value_label.setFont(font)
            column_value_label.setAlignment(QtCore.Qt.AlignCenter)
            column_value_label.setText(str(self.data_object[column_name]))
            column_values_layout.addWidget(column_value_label)
            i += 1
            if i > 20:
                column_names_layout = QHBoxLayout()
                column_values_layout = QHBoxLayout()
                attributes_layout.addLayout(column_names_layout)
                attributes_layout.addLayout(column_values_layout)
                i = 0

