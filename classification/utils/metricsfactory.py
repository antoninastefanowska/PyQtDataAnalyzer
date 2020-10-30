from .euclideandistance import EuclideanDistance
from .manhattandistance import ManhattanDistance
from .chebyshevdistance import ChebyshevDistance
from .mahalanobisdistance import MahalanobisDistance

class MetricsFactory:
    NAMES = [ "euklidesowa", "Manhattan", "Czebyszewa", "Mahalanobisa" ]

    def __init__(self):
        pass

    @staticmethod
    def get_by_name(name, data, class_column_name):
        index = MetricsFactory.NAMES.index(name)
        return MetricsFactory.get_by_id(index, data, class_column_name)

    @staticmethod
    def get_by_id(id, data, class_column_name):
        if id == 0:
            return EuclideanDistance()
        elif id == 1:
            return ManhattanDistance()
        elif id == 2:
            return ChebyshevDistance()
        elif id == 3:
            no_class_data = data.drop(class_column_name, axis=1)
            return MahalanobisDistance(no_class_data)

    @staticmethod
    def get_count():
        return len(MetricsFactory.NAMES)
