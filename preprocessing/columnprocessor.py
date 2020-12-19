import math

class ColumnProcessor:
    def __init__(self, column):
        self.column = column

    def text_to_numbers(self, method="alphabetically", cluster_column=None):
        strings = self.column.unique()
        dictionary = {}
        if method == "by_cluster":
            for value in strings:
                class_indices = self.column[self.column == value].index
                matching_clusters = cluster_column.take(class_indices)
                if matching_clusters.count() > 0:
                    label = matching_clusters.mode().iloc[0]
                    while label in dictionary.values():
                        matching_clusters = matching_clusters.drop(matching_clusters[matching_clusters == label].index)
                        if matching_clusters.count() > 0:
                            label = matching_clusters.mode().iloc[0]
                        else:
                            label = None
                            break
                    dictionary[value] = label

            for value in strings:
                if dictionary[value] is None:
                    label = 1
                    while label in dictionary.values():
                        label += 1
                    dictionary[value] = label
        else:
            if method == "alphabetically":
                strings.sort()
            label = 0
            for value in strings:
                label += 1
                dictionary[value] = label
        return self.column.map(dictionary)

    def discretize(self, bar_number):
        min = self.column.min()
        max = self.column.max()
        step = (max - min) / bar_number

        column = self.column.map(lambda value: int(math.ceil((value - min) / step)))
        column[column == 0] = 1
        return column

    def normalize(self):
        mean = self.column.mean()
        std = self.column.std()
        return self.column.map(lambda value: round((value - mean) / std, 4))

    def scale(self, a, b):
        min = self.column.min()
        max = self.column.max()
        return self.column.map(lambda value: round((b - a) * (value - min) / (max - min) + a, 4))