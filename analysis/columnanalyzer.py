class ColumnAnalyzer:
    def __init__(self, column):
        self.column = column

    def get_extremes_indexes(self, smallest_percent, biggest_percent):
        count = self.column.count()
        smallest_number = int(round(smallest_percent / 100 * count))
        biggest_number = int(round(biggest_percent / 100 * count))
        column = self.column.sort_values()

        smallest_indexes = column.index[:smallest_number]
        biggest_indexes = column.index[-biggest_number:]
        return smallest_indexes, biggest_indexes

    def compare(self, other_column, similarity_metrics):
        return similarity_metrics.get_similarity(self.column, other_column)