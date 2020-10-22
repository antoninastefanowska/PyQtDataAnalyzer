import pandas as pd

from .classifier import Classifier

class KNNClassifier(Classifier):
    def __init__(self, data, class_column_name, metrics, k):
        super().__init__(data, class_column_name)
        self.metrics = metrics
        self.k = k

    def classify(self, data_object):
        data_objects = []
        for index, row in self.data.iterrows():
            distance = self.metrics.get_distance(data_object, row)
            data_objects.append((row, distance))
        data_objects.sort(key=lambda x: x[1])
        neighbours = data_objects[:self.k]
        votes = {}

        for neighbour, distance in neighbours:
            class_value = neighbour[self.class_column_name]
            if class_value not in votes:
                votes[class_value] = 0
            votes[class_value] += 1

        max_votes = max(votes.items(), key=lambda x: x[1])
        winner = max_votes[0]
        maximum = max_votes[1]

        max_classes = []
        max_classes.append(winner)
        votes.pop(winner)

        for class_value in votes.keys():
            if votes[class_value] == maximum:
                max_classes.append(class_value)

        if len(max_classes) > 1:
            class_distances = {}
            for neighbour, distance in neighbours:
                class_value = neighbour[self.class_column_name]
                if class_value in max_classes:
                    if class_value not in class_distances:
                        class_distances[class_value] = 0
                    class_distances[class_value] += distance
            min_distance_class = min(class_distances.items(), key=lambda x: x[1])
            winner = min_distance_class

        return winner

