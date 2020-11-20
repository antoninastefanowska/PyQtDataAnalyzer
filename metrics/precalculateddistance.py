import numpy as np

from .distancemetrics import DistanceMetrics

class PrecalculatedDistance(DistanceMetrics):
    def __init__(self, data, class_column_name, metrics):
        super().__init__()
        self.data = data
        self.class_column_name = class_column_name
        self.metrics = metrics
        n = len(data.index)
        self.distance_matrix = np.zeros(shape=(n, n))

    def prepare(self):
        self.metrics.prepare()
        self.calculate_distance_matrix()

    def calculate_distance_matrix(self):
        for i, row1 in self.data.iterrows():
            for j, row2 in self.data.iterrows():
                if j < i:
                    row1_no_class = row1.drop(self.class_column_name)
                    row2_no_class = row2.drop(self.class_column_name)
                    self.distance_matrix[i][j] = self.metrics.get_distance(row1_no_class, row2_no_class)
                else:
                    break

    def get_distance(self, data_object1, data_object2):
        i = data_object1.name
        j = data_object2.name
        result = self.distance_matrix[i][j] if self.distance_matrix[i][j] != 0 else self.distance_matrix[j][i]
        return result

    def get_name(self):
        return self.metrics.get_name()