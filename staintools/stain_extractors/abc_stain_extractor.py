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
        """Estimate stain matrix given an image and relevant method parameters"""

    @staticmethod
    def get_concentrations(I, stain_matrix, **kwargs):
        """
        Estimate concentration matrix given an image, stain matrix and relevant method parameters

                Get the concentration matrix. Suppose the input image is H x W x 3 (uint8). Define Npix = H * W.
        Then the concentration matrix is Npix x 2 (or we could reshape to H x W x 2).
        The first element of each row is the Hematoxylin concentration.
        The second element of each row is the Eosin concentration.

        We do this by 'solving' OD = C*S (Matrix product) where OD is optical density (Npix x 3),\
        C is concentration (Npix x 2) and S is stain matrix (2 x 3).
        See docs for spams.lasso.

        We restrict the concentrations to be positive and penalise very large concentration values,\
        so that background pixels (which can not easily be expressed in the Hematoxylin-Eosin basis) have \
        low concentration and thus appear white.
        """
        n_stains = stain_matrix.shape[0]
        if n_stains == 2:
            OD = convert_RGB_to_OD(I).reshape((-1, 3))
            lasso_regularizer = kwargs['lasso_regularizer'] if 'lasso_regularizer' in kwargs.keys() else 0.01
            return spams.lasso(X=OD.T, D=stain_matrix.T, mode=2, lambda1=lasso_regularizer, pos=True).toarray().T
        elif n_stains == 3:
            OD = convert_RGB_to_OD(I).reshape((-1, 3))
            return np.linalg.solve(stain_matrix.T, OD.T).T
        else:
            raise Exception("Number of stains must be 2 or 3.")
