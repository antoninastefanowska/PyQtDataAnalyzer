import numpy as np

from .distancemetrics import DistanceMetrics

class EuclideanDistance(DistanceMetrics):
    def __init__(self):
        pass

    def get_distance(self, data_object1, data_object2):
        sum = 0.0
        if isinstance(data_object1, np.ndarray) and isinstance(data_object2, np.ndarray):
            for i, value1 in enumerate(data_object1):
                value2 = data_object2[i]
                sum += (value1 - value2) ** 2
        else:
            for column_name in data_object1.index:
                value1 = data_object1[column_name]
                value2 = data_object2[column_name]
                if (isinstance(value1, int) or isinstance(value1, float)) and (isinstance(value2, int) or isinstance(value2, float)):
                    sum += (value1 - value2)**2
        return np.sqrt(sum)

    def get_name(self):
        return "Euklides"
