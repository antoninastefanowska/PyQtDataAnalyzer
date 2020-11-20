import math

class ColumnProcessor:
    def __init__(self, column):
        self.column = column

    def text_to_numbers(self, alphabetically):
        strings = self.column.unique()
        if alphabetically:
            strings.sort()
        counter = 0
        dictionary = {}
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

    def get_extremes_indexes(self, smallest_percent, biggest_percent):
        count = self.column.count()
        smallest_number = int(round(smallest_percent / 100 * count))
        biggest_number = int(round(biggest_percent / 100 * count))
        column = self.column.sort_values()

        smallest_indexes = column.index[:smallest_number]
        biggest_indexes = column.index[-biggest_number:]
        return smallest_indexes, biggest_indexes