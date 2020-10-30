from .distancemetrics import DistanceMetrics

class ChebyshevDistance(DistanceMetrics):
    def __init__(self):
        pass

    def get_distance(self, data_object1, data_object2):
        max = 0.0
        for column_name in data_object1.index:
            value1 = data_object1[column_name]
            value2 = data_object2[column_name]
            if (isinstance(value1, int) or isinstance(value1, float)) and (isinstance(value2, int) or isinstance(value2, float)):
                diff = abs(value1 - value2)
                if diff > max:
                    max = diff
        return max

    def get_name(self):
        return "Czebyszew"
