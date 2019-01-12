from abc import ABC, abstractmethod


class ABCTissueLocator(ABC):

    @staticmethod
    @abstractmethod
    def get_tissue_mask(I):
        """
        Get a boolean tissue mask.

        :param I:
        :return:
        """