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
                dictionary[value] = matching_clusters.mode().iloc[0]
        else:
            if method == "alphabetically":
                strings.sort()
            counter = 0
            for value in strings:
                counter += 1
                dictionary[value] = counter
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