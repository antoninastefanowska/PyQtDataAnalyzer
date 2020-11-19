import pandas as pd
import numpy as np
from random import uniform

class KMeansClustering:
    def __init__(self, data, k, metrics, initialization_method="random"):
        self.data = data
        self.k = k
        self.metrics = metrics
        self.metrics.prepare()
        if initialization_method == "random":
            self.initial_centroids = self.initial_centroids_random
        elif initialization_method == "k-means++":
            self.initial_centroids = self.initial_centroids_kpp

    def initial_centroids_random(self):
        centroids = {}
        for i in range(1, self.k + 1):
            centroid = {}
            for column_name in self.data.columns:
                column = self.data[column_name]
                min = column.min()
                max = column.max()
                centroid[column_name] = uniform(min, max)
            centroids[i] = pd.Series(centroid)
        return centroids

    def initial_centroids_kpp(self):
        centroids = {}
        centroid = self.data.sample(n=1).iloc[0]
        centroids[1] = centroid
        probabilities = []

        sum_square_distance = 0
        for index, row in self.data.iterrows():
            distance = self.metrics.get_distance(row, centroid)
            square_distance = distance ** 2
            sum_square_distance += square_distance
            probabilities.append(square_distance / sum_square_distance)

        probabilities = np.array(probabilities)
        centroid = self.data.sample(n=1, weights=probabilities).iloc[0]
        centroids[2] = centroid

        labeled_data = pd.DataFrame()
        for i in range(2, self.k):
            labeled_data["distance"] = self.data.apply(lambda row: self.get_label(row, centroids)["distance"], axis=1)
            probabilities = []
            sum_square_distance = 0
            for index, row in self.data.iterrows():
                distance = self.metrics.get_distance(row, centroid)
                square_distance_new = distance ** 2
                square_distance = labeled_data.iloc[index]["distance"] ** 2
                sum_square_distance += square_distance
                probabilities.append(square_distance_new / sum_square_distance)

            probabilities = np.array(probabilities)
            centroid = self.data.sample(n=1, weights=probabilities).iloc[0]
            centroids[i + 1] = centroid
        return centroids

    def mean_centroids(self, centroids, labeled_data):
        for i in range(1, self.k + 1):
            cluster_rows = labeled_data[labeled_data["cluster"] == i]
            centroid = {}
            for column_name in self.data.columns:
                if column_name != "cluster":
                    column = cluster_rows[column_name]
                    mean = column.mean()
                    centroid[column_name] = mean
            centroids[i] = pd.Series(centroid)
        return centroids

    def get_label(self, row, centroids):
        distances = [{"distance": self.metrics.get_distance(row, centroids[key]), "label": key} for key in centroids.keys()]
        min_distance = min(distances, key=lambda x: x["distance"])
        return min_distance

    def k_means(self):
        centroids = self.initial_centroids()
        labeled_data = self.data.copy()
        last_labels = None
        while True:
            labeled_data["cluster"] = self.data.apply(lambda row: self.get_label(row, centroids)["label"], axis=1)
            if last_labels is not None and labeled_data["cluster"].equals(last_labels):
                break
            last_labels = labeled_data["cluster"]
            centroids = self.mean_centroids(centroids, labeled_data)

        return labeled_data["cluster"]
