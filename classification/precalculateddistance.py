import numpy as np

from .distancemetrics import DistanceMetrics

class PrecalculatedDistance(DistanceMetrics):
    def __init__(self, data, metrics):
        super().__init__()
        self.data = data
        self.metrics = metrics
        n = data.count()
        self.distance_matrix = np.zeros(shape=(n, n))

    def calculate_distance_matrix(self):
        for i, row1 in self.data.iterrows():
            for j, row2 in self.data.iterrows():
                if j < i:
                    self.distance_matrix[i][j] = metrics.get_distance(row1, row2)
                else:
                    break

    def get_distance(self, data_object1, data_object2):
        i = data_object1.get_loc()
        j = data_object2.get_loc()
        result = self.distance_matrix[i][j] if self.istance_matrix[i][j] != 0 else self.distance_matrix[j][i]
        return result
