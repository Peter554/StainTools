from abc import ABC, abstractmethod


class ABCStainExtractor(ABC):

    @staticmethod
    @abstractmethod
    def get_stain_matrix(I):
        """
        Estimate the stain matrix given an image.

        :param I:
        :return:
        """

