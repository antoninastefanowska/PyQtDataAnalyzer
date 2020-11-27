from .jaccardsimilarity import JaccardSimilarity
from .dicesimilarity import DiceSimilarity
from .smcsimilarity import SMCSimilarity

class SimilarityFactory:
    NAMES = ["Jaccard", "Dice", "SMC"]

    def __init__(self):
        pass

    @staticmethod
    def get_by_name(name):
        index = SimilarityFactory.NAMES.index(name)
        return SimilarityFactory.get_by_id(index)

    @staticmethod
    def get_by_id(id):
        if id == 0:
            return JaccardSimilarity()
        elif id == 1:
            return DiceSimilarity()
        elif id == 2:
            return SMCSimilarity()