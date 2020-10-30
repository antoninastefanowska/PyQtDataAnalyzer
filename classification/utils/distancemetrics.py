from abc import ABC, abstractmethod

class DistanceMetrics(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_distance(self, data_object1, data_object2):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def update_data(self, data):
        pass

    def prepare(self):
        pass
