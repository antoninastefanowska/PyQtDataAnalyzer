from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QRunnable

class TestingWorker(QRunnable):
    def __init__(self, tester, classifier):
        super().__init__()
        self.tester = tester
        self.tester.set_progress_callback(self.progress_callback)
        self.classifier = classifier
        self.signals = TestingWorker.TestingSignals()

    @pyqtSlot()
    def run(self):
        result = self.tester.test_classifier(self.classifier)
        self.signals.result.emit(result)

    def progress_callback(self, progress):
        self.signals.progress.emit(progress)

    class TestingSignals(QObject):
        progress = pyqtSignal(int)
        result = pyqtSignal(int)
