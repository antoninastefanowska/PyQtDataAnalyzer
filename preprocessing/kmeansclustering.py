import pandas as pd
from random import uniform

class KMeansClustering:
    def __init__(self, data, k, metrics):
        self.data = data
        self.k = k
        self.metrics = metrics
        self.metrics.prepare()
        self.centroids = None

    def random_centroid(self):
        centroid = {}
        for column_name in self.data.columns:
            column = self.data[column_name]
            min = column.min()
            max = column.max()
            centroid[column_name] = uniform(min, max)
        return pd.Series(centroid)

    def mean_centroid(self, cluster_rows):
        centroid = {}
        for column_name in self.data.columns:
            if column_name != "cluster":
                column = cluster_rows[column_name]
                mean = column.mean()
                centroid[column_name] = mean
        return pd.Series(centroid)

    def get_label(self, row):
        distances = [{"distance": self.metrics.get_distance(row, self.centroids[key]), "label": key} for key in self.centroids.keys()]
        min_distance = min(distances, key=lambda x: x["distance"])
        return min_distance["label"]

    def k_means(self):
        self.centroids = {}
        for i in range(1, self.k + 1):
            self.centroids[i] = self.random_centroid()

        labeled_data = self.data.copy()
        last_labels = None
        while True:
            labeled_data["cluster"] = self.data.apply(self.get_label, axis=1)
            if last_labels is not None and labeled_data["cluster"].equals(last_labels):
                break
            last_labels = labeled_data["cluster"]

            for i in range(1, self.k + 1):
                cluster_rows = labeled_data[labeled_data["cluster"] == i]
                self.centroids[i] = self.mean_centroid(cluster_rows)
        return labeled_data["cluster"]
