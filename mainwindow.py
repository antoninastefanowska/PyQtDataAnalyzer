from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableView
from PyQt5.QtCore import pyqtSlot

from data.tablemodel import TableModel
from data.loaddatadialog import LoadDataDialog

from column.texttonumberdialog import TextToNumberDialog
from column.discretizedialog import DiscretizeDialog
from column.normalizedialog import NormalizeDialog
from column.normalizealldialog import NormalizeAllDialog
from column.scaledialog import ScaleDialog
from column.highlightdialog import HighlightDialog
from column.classcolumndialog import ClassColumnDialog

from visualization.chart2ddialog import Chart2DDialog
from visualization.chart3ddialog import Chart3DDialog
from visualization.histogramdialog import HistogramDialog
from visualization.chartcanvas import ChartCanvas
from visualization.chartwindow import ChartWindow

from classification.utils.knnclassifier import KNNClassifier
from classification.knnclassifierdialog import KNNClassifierDialog
from classification.knntestingmanager import KNNTestingManager
from classification.newobjectdialog import NewObjectDialog
from classification.classificationresultwindow import ClassificationResultWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.data = None
        self.table_model = None
        self.load_ui()
        self.testing_manager = None

    def load_ui(self):
        uic.loadUi("ui/mainwindow.ui", self)

    @pyqtSlot()
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Otwórz...", "", "Wszystkie pliki (*);;Pliki CSV (*.csv);;Pliki tekstowe (*.txt)", options=QFileDialog.Options())
        if filename:
            dialog = LoadDataDialog(self, filename)
            if dialog.exec_():
                table_view = self.findChild(QTableView, "tableView")
                self.data = dialog.data
                self.table_model = TableModel(self.data)
                table_view.setModel(self.table_model)

    @pyqtSlot()
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Zapisz jako...", "", "Wszystkie pliki (*);;Pliki CSV (*.csv);;Pliki tekstowe (*.txt)", options=QFileDialog.Options())
        if filename:
            self.data.to_csv(filename, sep=';', header=True, index=False)

    @pyqtSlot()
    def text_to_numbers(self):
        dialog = TextToNumberDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def discretize(self):
        dialog = DiscretizeDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def normalize(self):
        dialog = NormalizeDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def normalize_all(self):
        dialog = NormalizeAllDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def scale(self):
        dialog = ScaleDialog(self, self.data)
        if dialog.exec_():
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def highlight(self):
        dialog = HighlightDialog(self, self.data)
        if dialog.exec_():
            self.table_model.green_rows = dialog.smallest_indexes
            self.table_model.red_rows = dialog.biggest_indexes
            self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def remove(self):
        table_view = self.findChild(QTableView, "tableView")
        selected_columns = table_view.selectionModel().selectedColumns()
        columns = [self.data.columns[index.column()] for index in selected_columns]
        self.data = self.data.drop(columns, axis='columns')
        self.table_model.set_data(self.data)
        self.table_model.layoutChanged.emit()

    @pyqtSlot()
    def show_chart2d(self):
        chart_canvas = ChartCanvas(subplots=1)
        chart = chart_canvas.get_subplot(0)
        dialog = Chart2DDialog(self, self.data, chart)
        if dialog.exec_():
            chart_window = ChartWindow(self, chart_canvas)
            chart_window.show()

    @pyqtSlot()
    def show_chart3d(self):
        chart_canvas = ChartCanvas(subplots=1, projection="3d")
        chart = chart_canvas.get_subplot(0)
        dialog = Chart3DDialog(self, self.data, chart)
        if dialog.exec_():
            chart_window = ChartWindow(self, chart_canvas)
            chart_window.show()

    @pyqtSlot()
    def show_histogram(self):
        chart_canvas = ChartCanvas(subplots=1)
        chart = chart_canvas.get_subplot(0)
        dialog = HistogramDialog(self, self.data, chart)
        if dialog.exec_():
            chart_window = ChartWindow(self, chart_canvas)
            chart_window.show()

    @pyqtSlot()
    def classify_knn_method(self):
        dialog = KNNClassifierDialog(self, self.data)
        if dialog.exec_():
            class_column_name = dialog.class_column_name
            metrics = dialog.metrics
            k_value = dialog.k_value
            new_object_dialog = NewObjectDialog(self, self.data, class_column_name)

            if new_object_dialog.exec_():
                new_object = new_object_dialog.new_object
                classifier = KNNClassifier(self.data, class_column_name, metrics, k_value)
                classifier.prepare()
                result = classifier.classify(new_object)
                result_window = ClassificationResultWindow(self, new_object, class_column_name, result)
                result_window.show()

    @pyqtSlot()
    def test_knn_method(self):
        dialog = KNNClassifierDialog(self, self.data)
        if dialog.exec_():
            class_column_name = dialog.class_column_name
            metrics = dialog.metrics
            k_value = dialog.k_value

            self.testing_manager = KNNTestingManager(self, self.data, class_column_name)
            self.testing_manager.run_single_test(k_value, metrics)

    @pyqtSlot()
    def test_knn_parameters(self):
        dialog = ClassColumnDialog(self, self.data)
        if dialog.exec_():
            class_column_name = dialog.class_column_name
            self.testing_manager = KNNTestingManager(self, self.data, class_column_name)
            self.testing_manager.run_parameter_testing()
