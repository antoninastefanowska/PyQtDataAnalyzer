import pandas as pd
from random import uniform
from sklearn.cluster import KMeans

from yellowbrick.cluster import SilhouetteVisualizer

class KMeansClustering:
    def __init__(self, data, k, metrics, initialization_method="random"):
        self.data = data
        self.k = k
        self.metrics = metrics
        if initialization_method == "random":
            self.initial_centroids = self.initial_centroids_random
        elif initialization_method == "k-means++":
            self.initial_centroids = self.initial_centroids_kpp
        self.distance_sums = None

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

        calculations = pd.DataFrame()
        calculations["square_distance"] = self.data.apply(lambda row: self.get_cluster(row, centroids)["distance"] ** 2, axis=1)
        sum = calculations["square_distance"].sum()
        calculations["probability"] = calculations.apply(lambda row: row["square_distance"] / sum, axis=1)

        centroid = self.data.sample(n=1, weights=calculations["probability"]).iloc[0]
        centroids[2] = centroid
        for i in range(3, self.k + 1):
            calculations["square_distance"] = self.data.apply(lambda row: self.get_cluster(row, centroids)["distance"] ** 2, axis=1)
            sum = calculations["square_distance"].sum()
            calculations["probability"] = calculations.apply(lambda row: row["square_distance"] / sum, axis=1)

            centroid = self.data.sample(n=1, weights=calculations["probability"]).iloc[0]
            centroids[i] = centroid

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

    def calculate_distance_sums(self, labeled_data):
        self.distance_sums = {}
        for k in range(1, self.k + 1):
            cluster = labeled_data[labeled_data["cluster"] == k]
            distance_sums = []
            for i, row1 in cluster.iterrows():
                distance_sum = 0
                for j, row2 in cluster.iterrows():
                    if i != j:
                        actual_row1 = self.data.loc[i]
                        actual_row2 = self.data.loc[j]
                        distance_sum += self.metrics.get_distance(actual_row1, actual_row2)
                distance_sums.append(distance_sum)
            self.distance_sums[k] = distance_sums

    def silhouette_function(self, labeled_data, cluster_label):
        cluster = labeled_data[labeled_data["cluster"] == cluster_label]
        sum_s = 0
        for i, row in cluster.iterrows():
            a = 1 / (len(cluster) - 1) * self.distance_sums[cluster_label][i]
            b = -1
            for k in range(1, self.k + 1):
                if k != cluster_label:
                    other_cluster = labeled_data[labeled_data["cluster"] == k]
                    count = len(other_cluster)
                    for j, row2 in other_cluster.iterrows():
                        value = 1 / count * self.distance_sums[k][j]
                    if b == -1 or b > value:
                        b = value
            if a < b:
                s = 1 - a / b
            elif a == b:
                s = 0
            else:
                s = b / a - 1
            sum_s += s
        return sum_s / self.k

    def calculate_optimality(self, labeled_data):
        self.calculate_distance_sums(labeled_data)
        max = 0
        for i in range(1, self.k + 1):
            silhouette_mean = self.silhouette_function(labeled_data, i)
            if max < silhouette_mean:
                max = silhouette_mean
        return max

    def get_cluster(self, row, centroids):
        distances = [{"distance": self.metrics.get_distance(row, centroids[key]), "label": key} for key in centroids.keys()]
        cluster = min(distances, key=lambda x: x["distance"])
        return cluster

    def k_means(self):
        centroids = self.initial_centroids()
        labeled_data = self.data.copy()
        last_labels = None
        while True:
            labeled_data["cluster"] = self.data.apply(lambda row: self.get_cluster(row, centroids)["label"], axis=1)
            if last_labels is not None and labeled_data["cluster"].equals(last_labels):
                break
            last_labels = labeled_data["cluster"]
            centroids = self.mean_centroids(centroids, labeled_data)

        return labeled_data["cluster"]

    def visualize(self):
        model = KMeans(self.k)
        visualizer = SilhouetteVisualizer(model, colors='yellowbrick')
        visualizer.fit(self.data)
        visualizer.show()