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

    def get_intersection_count(self, column1, column2):
        intersection_count = 0
        unique1 = column1.unique()
        unique2 = column2.unique()
        unique = unique2 if len(unique1) > len(unique2) else unique1

        for value in unique:
            count1 = column1[column1 == value].count()
            count2 = column2[column2 == value].count()
            intersection_count += count2 if count1 > count2 else count1

        return intersection_count