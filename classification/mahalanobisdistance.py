import numpy as np

from .distancemetrics import DistanceMetrics

class MahalanobisDistance(DistanceMetrics):
    def __init__(self, data):
        self.inv_cov_matrix = None
        self.calculate_inv_cov_matrix(data)

    def calculate_inv_cov_matrix(self, data):
        cov_df = data.cov()
        cov_matrix = cov_df.to_numpy()
        self.inv_cov_matrix = np.linalg.inv(cov_matrix)

    def get_distance(self, data_object1, data_object2):
        vec1 = data_object1.values
        vec2 = data_object2.values

        diff = vec1 - vec2
        diff1 = diff.reshape(1, len(diff))
        diff2 = diff.reshape(-1, 1)

        product1 = np.dot(self.inv_cov_matrix, diff2)
        product2 = np.dot(diff1, product1)
        return np.sqrt(product2[0][0])
