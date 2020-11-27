from .euclideandistance import EuclideanDistance
from .manhattandistance import ManhattanDistance
from .chebyshevdistance import ChebyshevDistance
from .mahalanobisdistance import MahalanobisDistance

class MetricsFactory:
    NAMES = [ "euklidesowa", "Manhattan", "Czebyszewa", "Mahalanobisa" ]

    def __init__(self):
        pass

    @staticmethod
    def get_by_name(name, data):
        index = MetricsFactory.NAMES.index(name)
        return MetricsFactory.get_by_id(index, data)

    @staticmethod
    def get_by_id(id, data):
        if id == 0:
            return EuclideanDistance()
        elif id == 1:
            return ManhattanDistance()
        elif id == 2:
            return ChebyshevDistance()
        elif id == 3:
            return MahalanobisDistance(data)

    @staticmethod
    def get_count():
        return len(MetricsFactory.NAMES)
