from abc import ABC, abstractmethod


class ABCStainExtractor(ABC):

    @staticmethod
    @abstractmethod
    def get_stain_matrix(I, *args, **kwargs):
        """
        Estimate the stain matrix given an image.
        """

