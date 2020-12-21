from PyQt5.QtCore import QThreadPool

from classification.gui.testingresultwindow import TestingResultWindow
from .testingworker import TestingWorker
from ..gui.progresswindow import ProgressWindow

class TestingManager:
    def __init__(self, context, data, class_column_name):
        self.context = context
        self.data = data
        self.class_column_name = class_column_name

        self.progress_window = None
        self.test_count = 0
        self.all_results = []

    def run_single_test(self, tester, classifier):
        worker = TestingWorker(tester, classifier, classifier.get_main_param())
        worker.signals.result.connect(self.show_single_testing_result)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.status.connect(self.update_status)

        self.progress_window = ProgressWindow(self.context)
        self.progress_window.show()
        QThreadPool.globalInstance().start(worker)

    def show_single_testing_result(self, result):
        result_window = TestingResultWindow(self.context, self.data, result)
        result_window.show()
        self.progress_window.finish()
        self.progress_window = None

    def update_progress(self, progress):
        self.progress_window.update(progress)

    def update_status(self, status):
        self.progress_window.update_status(status)
