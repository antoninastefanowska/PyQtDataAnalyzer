import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

class NewObjectDialog(QDialog):
    def __init__(self, parent, data, class_column_name):
        super().__init__(parent)
        self.data = data
        self.class_column_name = class_column_name
        self.column_names = None
        self.new_object = None
        self.textboxes = {}
        self.load_ui()

    def load_ui(self):
        uic.loadUi("ui/newobjectdialog.ui", self)
        labels_layout = self.findChild(QVBoxLayout, "labelsLayout")
        textboxes_layout = self.findChild(QVBoxLayout, "textboxesLayout")
        attributes_layout = self.findChild(QHBoxLayout, "attributesLayout")

        self.column_names = self.data.columns
        self.column_names = self.column_names[self.column_names != self.class_column_name]
        i = 0
        for column_name in self.column_names:
            label = QLabel()
            label.setText(column_name)
            textbox = QLineEdit()
            labels_layout.addWidget(label)
            textboxes_layout.addWidget(textbox)
            self.textboxes[column_name] = textbox
            i += 1
            if i > 20:
                labels_layout = QVBoxLayout()
                textboxes_layout = QVBoxLayout()
                attributes_layout.addLayout(labels_layout)
                attributes_layout.addLayout(textboxes_layout)
                i = 0

    def create_new_object(self):
        new_object_dict = {}
        for column_name in self.textboxes:
            new_object_dict[column_name] = self.textboxes[column_name].text()
        df = pd.DataFrame(new_object_dict, index=[0])
        df = df.apply(pd.to_numeric, errors="coerce").fillna(df)
        self.new_object = df.iloc[0]

    @pyqtSlot()
    def accept(self):
        self.create_new_object()
        super().accept()
