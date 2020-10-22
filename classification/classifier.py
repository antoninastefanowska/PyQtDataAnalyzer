from abc import ABC, abstractmethod

class Classifier(ABC):
    def __init__(self, data, class_column_name):
        self.data = data
        self.class_column_name = class_column_name

    @abstractmethod
    def classify(self, data_object):
        pass
