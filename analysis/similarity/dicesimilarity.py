from .similaritymetrics import SimilarityMetrics

class DiceSimilarity(SimilarityMetrics):
    def __init__(self):
        pass

    def get_similarity(self, column1, column2):
        intersection_count = self.get_intersection_count(column1, column2)
        return 2 * intersection_count / (column1.count() + column2.count())