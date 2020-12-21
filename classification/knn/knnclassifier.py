from classification.classifier import Classifier

class KNNClassifier(Classifier):
    def __init__(self, data, class_column_name, metrics, k=None):
        super().__init__(data, class_column_name)
        self.metrics = metrics
        self.k = k

    def prepare_for_testing(self):
        self.metrics.prepare()

    def build(self):
        self.metrics.prepare()

    def set_parameter(self, parameter):
        self.k = parameter

    def get_param_string(self):
        return "K: " + str(self.k) + " Metryka: " + self.metrics.get_name()

    def get_result_info_string(self):
        return "K: " + str(self.k) + "\nMetryka: " + self.metrics.get_name()

    def get_param_list(self):
        params = []
        params.append(("K", str(self.k)))
        params.append(("Metryka", self.metrics.get_name()))
        return params

    def get_name(self):
        return "KNN"

    def classify(self, data_object):
        data_objects = []
        for index, row in self.data.iterrows():
            row_no_class = row.drop(self.class_column_name)
            distance = self.metrics.get_distance(data_object, row_no_class)
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
            winner = min_distance_class[0]

        return winner

    def get_main_param(self):
        return [self.k]