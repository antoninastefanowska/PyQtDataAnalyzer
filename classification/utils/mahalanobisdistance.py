import numpy as np

from .distancemetrics import DistanceMetrics

class MahalanobisDistance(DistanceMetrics):
    def __init__(self, data):
        self.inv_cov_matrix = None
        self.data = data

    def update_data(data):
        self.data = data
        self.prepare()

    def prepare(self):
        self.calculate_inv_cov_matrix(self.data)

    def calculate_inv_cov_matrix(self, data):
        cov_df = data.cov()
        cov_matrix = cov_df.to_numpy()
        try:
            self.inv_cov_matrix = np.linalg.inv(cov_matrix)
        except np.linalg.LinAlgError:
            self.inv_cov_matrix = np.linalg.pinv(cov_matrix)

    def get_distance(self, data_object1, data_object2):
        vec1 = data_object1.values
        vec2 = data_object2.values
        self.remove_strings(vec1)
        self.remove_strings(vec2)

        diff = vec1 - vec2
        diff1 = diff.reshape(1, len(diff))
        diff2 = diff.reshape(-1, 1)

        product1 = np.dot(self.inv_cov_matrix, diff2)
        product2 = np.dot(diff1, product1)
        return np.sqrt(product2[0][0])

    def remove_strings(self, vec):
        removed = []
        i = 0
        for val in vec:
            if isinstance(val, str):
                removed.append(i)
            i += 1
        vec = np.delete(vec, removed)
