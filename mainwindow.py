from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableView, QLabel
from PyQt5.QtCore import pyqtSlot, QThreadPool

from data.tablemodel import TableModel
from data.loaddatadialog import LoadDataDialog

from column.texttonumberdialog import TextToNumberDialog
from column.discretizedialog import DiscretizeDialog
from column.normalizedialog import NormalizeDialog
from column.scaledialog import ScaleDialog
from column.highlightdialog import HighlightDialog

from visualization.chart2ddialog import Chart2DDialog
from visualization.chart3ddialog import Chart3DDialog
from visualization.histogramdialog import HistogramDialog
from visualization.chartcanvas import ChartCanvas

from classification.utils.knnclassifier import KNNClassifier
from classification.utils.leaveoneouttester import LeaveOneOutTester
from classification.utils.precalculateddistance import PrecalculatedDistance

from classification.knnclassifierdialog import KNNClassifierDialog
from classification.newobjectdialog import NewObjectDialog
from classification.classificationresultwindow import ClassificationResultWindow
from classification.testingresultwindow import TestingResultWindow
from classification.testingworker import TestingWorker
from classification.progresswindow import ProgressWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.data = None
        self.table_model = None
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(2)
        self.progress_window = None
        self.load_ui()

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
    def show_chart2d(self):
        chart_canvas = ChartCanvas()
        chart = chart_canvas.axes
        dialog = Chart2DDialog(self, self.data, chart)
        if dialog.exec_():
            new_window = QMainWindow(self)
            new_window.setWindowTitle("Wykres")
            new_window.setCentralWidget(chart_canvas)
            new_window.show()

    @pyqtSlot()
    def show_chart3d(self):
        chart_canvas = ChartCanvas(projection="3d")
        chart = chart_canvas.axes
        dialog = Chart3DDialog(self, self.data, chart)
        if dialog.exec_():
            new_window = QMainWindow(self)
            new_window.setWindowTitle("Wykres")
            new_window.setCentralWidget(chart_canvas)
            new_window.show()

    @pyqtSlot()
    def show_histogram(self):
        chart_canvas = ChartCanvas()
        chart = chart_canvas.axes
        dialog = HistogramDialog(self, self.data, chart)
        if dialog.exec_():
            new_window = QMainWindow(self)
            new_window.setWindowTitle("Wykres")
            new_window.setCentralWidget(chart_canvas)
            new_window.show()

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

            distances = PrecalculatedDistance(self.data, class_column_name, metrics)
            classifier = KNNClassifier(self.data, class_column_name, distances, k_value)
            tester = LeaveOneOutTester(self.data, class_column_name)

            worker = TestingWorker(tester, classifier)
            worker.signals.result.connect(self.show_testing_result)
            worker.signals.progress.connect(self.update_progress)
            worker.signals.status.connect(self.update_status)
            self.progress_window = ProgressWindow(self)
            self.progress_window.show()
            self.threadpool.start(worker)

    def show_testing_result(self, result):
        result_window = TestingResultWindow(self, self.data, result)
        result_window.show()
        self.progress_window.finish()
        self.progress_window = None

    def update_progress(self, progress):
        self.progress_window.update(progress)

    def update_status(self, status):
        self.progress_window.update_status(status)
