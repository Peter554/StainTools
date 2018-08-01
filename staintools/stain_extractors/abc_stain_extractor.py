from __future__ import division

from abc import ABC, abstractmethod
import numpy as np
import spams

from staintools.utils.misc_utils import convert_RGB_to_OD


class StainExtractor(ABC):
    """
    A stain extractor provides methods for estimating the stain matrix and concentration matrix.
    """

    @abstractmethod
    def get_stain_matrix(self, I, *args):
        """
        Estimate stain matrix given an image and relevant method parameters
        """

    @staticmethod
    def get_concentrations(I, stain_matrix, **kwargs):
        """
        Estimate concentration matrix given an image, stain matrix and relevant method parameters.
        """
        OD = convert_RGB_to_OD(I).reshape((-1, 3))
        lasso_regularizer = kwargs['lasso_regularizer'] if 'lasso_regularizer' in kwargs.keys() else 0.01
        return spams.lasso(X=OD.T, D=stain_matrix.T, mode=2, lambda1=lasso_regularizer, pos=True).toarray().T
