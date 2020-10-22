from abc import ABC, abstractmethod

class DistanceMetrics(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_distance(self, data_object1, data_object2):
        pass
