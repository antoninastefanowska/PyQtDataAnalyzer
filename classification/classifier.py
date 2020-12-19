from abc import ABC, abstractmethod

class Classifier(ABC):
    def __init__(self, data, class_column_name):
        self.data = data
        self.class_column_name = class_column_name

    def update_data(self, data):
        self.data = data

    @abstractmethod
    def classify(self, data_object):
        pass

    @abstractmethod
    def get_param_string(self):
        pass

    @abstractmethod
    def get_result_info_string(self):
        pass

    @abstractmethod
    def get_param_list(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def set_parameter(self, parameter):
        pass

    def prepare(self):
        pass

    def get_classifier_output_data(self):
        return None
