from abc import ABC, abstractmethod


class ABCTissueLocator(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def get_tissue_mask(I, **kwargs):
        """

        """