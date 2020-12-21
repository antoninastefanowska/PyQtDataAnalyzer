import pandas as pd

from classification.classifier import Classifier
from .hyperplane import Hyperplane

class HyperplaneClassifier(Classifier):
    def __init__(self, data, class_column_name):
        super().__init__(data, class_column_name)
        self.hyperplanes = []
        self.removed_count = 0

    def build(self):
        column_names = self.data.columns[self.data.columns != self.class_column_name]
        current_data = self.data
        while True:
            max = 0
            for column_name in column_names:
                sorted_data = current_data.sort_values(by=[column_name, self.class_column_name])

                separated_negative, point_negative, class_negative, removed_negative = self.separate_data(sorted_data, column_name)

                if len(current_data) == len(separated_negative):
                    return

                separated_positive, point_positive, class_positive, removed_positive = self.separate_data(sorted_data[::-1], column_name)

                if len(separated_negative) > max:
                    max = len(separated_negative)
                    max_hyperplane = Hyperplane(0, point_negative, column_name, class_negative)
                    max_removed = removed_negative
                    max_separated_data = separated_negative

                if len(separated_positive) > max:
                    max = len(separated_positive)
                    max_hyperplane = Hyperplane(1, point_positive, column_name, class_positive)
                    max_removed = removed_positive
                    max_separated_data = separated_positive

            self.hyperplanes.append(max_hyperplane)
            self.removed_count += max_removed
            current_data = current_data.drop([row.name for row in max_separated_data])

    def update_data(self, data):
        super().update_data(data)
        self.build()

    def separate_data(self, data, column_name):
        old_class_value = None
        point = None
        class_value = None
        removed_count = 0
        separated = []
        for index, row in data.iterrows():
            if old_class_value == None:
                old_class_value = row[self.class_column_name]
                old_point = row[column_name]
                separated.append(row)
                continue

            new_class_value = row[self.class_column_name]
            new_point = row[column_name]

            if new_class_value == old_class_value:
                separated.append(row)
            else:
                class_value = old_class_value
                point = (new_point - old_point) / 2 + old_point

                if new_point == old_point:
                    removed = data[(data[column_name] == point) & (data[self.class_column_name] != class_value)]
                    removed_count += len(removed)
                    data = data.drop(removed.index)

                break

            old_class_value = new_class_value
            old_point = new_point

        return separated, point, class_value, removed_count

    def classify(self, data_object):
        for vector in self.hyperplanes:
            if vector.in_area(data_object):
                return vector.class_value

    def get_vectorized_data(self):
        column_names = []
        for i in range(1, len(self.hyperplanes) + 1):
            column_names.append("v" + str(i))
        column_names.append(self.class_column_name)

        vectorized_dict = {}
        i = 0
        for vector in self.hyperplanes:
            column = []
            for index, row in self.data.iterrows():
                column.append(int(vector.in_area(row)))
            vectorized_dict[column_names[i]] = column
            i += 1

        vectorized_data = pd.DataFrame(vectorized_dict)
        vectorized_data[self.class_column_name] = self.data[self.class_column_name]
        return vectorized_data

    def get_classifier_output_data(self):
        return self.get_vectorized_data()

    def get_param_string(self):
        return ""

    def get_result_info_string(self):
        return "Długość wektora: " + str(len(self.hyperplanes)) + "\nLiczba usuniętych wartości: " + str(self.removed_count)

    def get_param_list(self):
        params = []
        params.append(("Długość wektora", str(len(self.hyperplanes))))
        params.append(("Usunięte", str(self.removed_count)))
        return params

    def get_name(self):
        return "Hiperpłaszczyzny"