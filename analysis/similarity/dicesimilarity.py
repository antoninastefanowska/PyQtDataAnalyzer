from .similaritymetrics import SimilarityMetrics

class DiceSimilarity(SimilarityMetrics):
    def __init__(self):
        pass

    def get_similarity(self, column1, column2):
        matching_count = self.get_matching_count(column1, column2)
        return 2 * matching_count / (2 * column1.count())