from abc import ABC, abstractmethod

class ClassifierTester(ABC):
    def __init__(self, data, class_column_name):
        self.data = data
        self.class_column_name = class_column_name
        self.progress_callback = None
        self.status_callback = None
        self.progress = 0

    @abstractmethod
    def test_classifier(self, classifier):
        pass

    @abstractmethod
    def prepare(self, classifier):
        pass

    def set_progress_callback(self, progress_callback):
        self.progress_callback = progress_callback

    def set_status_callback(self, status_callback):
        self.status_callback = status_callback
