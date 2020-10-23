from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QRunnable

class TestingWorker(QRunnable):
    def __init__(self, tester, classifier):
        super().__init__()
        self.tester = tester
        self.tester.set_progress_callback(self.progress_callback)
        self.tester.set_status_callback(self.status_callback)
        self.classifier = classifier
        self.signals = TestingWorker.TestingSignals()

    @pyqtSlot()
    def run(self):
        result = self.tester.test_classifier(self.classifier)
        self.signals.result.emit(result)

    def progress_callback(self, progress):
        self.signals.progress.emit(progress)

    def status_callback(self, status):
        self.signals.status.emit(status)

    class TestingSignals(QObject):
        progress = pyqtSignal(int)
        status = pyqtSignal(str)
        result = pyqtSignal(int)
