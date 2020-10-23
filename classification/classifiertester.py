from abc import ABC, abstractmethod

class ClassifierTester(ABC):
    def __init__(self, data, class_column_name):
        self.data = data
        self.class_column_name = class_column_name
        self.progress_callback = None

    @abstractmethod
    def test_classifier(self, classifier):
        pass

    def set_progress_callback(self, progress_callback):
        self.progress_callback = progress_callback
