from PyQt5.QtCore import QThreadPool

from ..testingworker import TestingWorker
from ..progresswindow import ProgressWindow

from ..utils.testingmanager import TestingManager
from ..utils.leaveoneouttester import LeaveOneOutTester

from .classifier.hyperplaneclassifier import HyperplaneClassifier

class HyperplaneTestingManager(TestingManager):
    def __init__(self, context, data, class_column_name):
        super().__init__(context, data, class_column_name)

    def run_single_test(self):
        classifier = HyperplaneClassifier(self.data, self.class_column_name)
        tester = LeaveOneOutTester(self.data, self.class_column_name)

        worker = TestingWorker(tester, classifier, [None])
        worker.signals.result.connect(self.show_single_testing_result)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.status.connect(self.update_status)

        self.progress_window = ProgressWindow(self.context)
        self.progress_window.show()
        QThreadPool.globalInstance().start(worker)

