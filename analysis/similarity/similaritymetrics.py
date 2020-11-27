from abc import ABC, abstractmethod

class SimilarityMetrics(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_similarity(self, column1, column2):
        pass

    def get_matching_count(self, column1, column2):
        matching_count = 0
        for index, value in column1.items():
            if value == column2.loc[index]:
                matching_count += 1
        return matching_count