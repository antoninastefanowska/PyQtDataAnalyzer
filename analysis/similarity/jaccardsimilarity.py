from .similaritymetrics import SimilarityMetrics

class JaccardSimilarity(SimilarityMetrics):
    def __init__(self):
        pass

    def get_similarity(self, column1, column2):
        matching_count = self.get_matching_count(column1, column2)
        return matching_count / (2 * column1.count() - matching_count)