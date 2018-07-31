"""
Normalizer abstract base classes
"""

from __future__ import division

from abc import ABC, abstractmethod
import spams
import numpy as np

from staintools.utils.misc import convert_RGB_to_OD, convert_OD_to_RGB


class Normaliser(ABC):
    """
    Abstract base class for normalizers. Defines some necessary methods to be considered a normalizer.
    """
    
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, target):
        """Fit the normalizer to an target image"""

    @abstractmethod
    def transform(self, I):
        """Transform an image to the target stain"""


class StainNormalizer(Normaliser):
    """
    Abstract class for a stain normalizer (inherits from Normalizer).
    Implements fit and transorm methods.
    Adds other methods including methods to estimate stain and concentration matrix.
    """

    def __init__(self):
        super().__init__()
        self.stain_matrix_target = None
        self.target_concentrations = None

    def fit(self, target):
        """
        Fit to a target image.

        :param target: Image RGB uint8.
        :return:
        """
        self.stain_matrix_target = self.get_stain_matrix(target)
        self.target_concentrations = self.get_concentrations(target, self.stain_matrix_target)

    def transform(self, I):
        """
        Transform an image.

        :param I: Image RGB uint8.
        :return:
        """
        stain_matrix_source = self.get_stain_matrix(I)
        source_concentrations = self.get_concentrations(I, stain_matrix_source)
        assert stain_matrix_source.min() >= 0, "Stain matrix has negative values."
        assert source_concentrations.min() >= 0, "Concentration matrix has negative values."
        maxC_source = np.percentile(source_concentrations, 99, axis=0).reshape((1, 2))
        maxC_target = np.percentile(self.target_concentrations, 99, axis=0).reshape((1, 2))
        source_concentrations *= (maxC_target / maxC_source)
        tmp = 255 * np.exp(-1 * np.dot(source_concentrations, self.stain_matrix_target))
        return tmp.reshape(I.shape).astype(np.uint8)

    def fetch_target_stains(self):
        """
        Fetch the target stain matrix and convert from OD to RGB.
        Must call fit first (this builds the stain matrix).

        :return:
        """
        assert self.stain_matrix_target is not None, "Run fit method first."
        return convert_OD_to_RGB(self.stain_matrix_target)

    def get_hematoxylin(self, I):
        """
        Hematoxylin channel extraction.

        :param I: Image RGB uint8.
        :return:
        """
        h, w, c = I.shape
        stain_matrix_source = self.get_stain_matrix(I)
        source_concentrations = self.get_concentrations(I, stain_matrix_source)
        H = source_concentrations[:, 0].reshape(h, w)
        H = np.exp(-1 * H)
        return H

    @abstractmethod
    def get_stain_matrix(self, I, *args):
        """Estimate stain matrix given an image and relevant method parameters"""

    @staticmethod
    def get_concentrations(I, stain_matrix, lamda=0.01):
        """
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

        :param I: Image. A np array H x W x 3 of type uint8.
        :param stain_matrix: a 2 x 3 stain matrix. First row is Hematoxylin stain vector, second row is Eosin stain vector.
        :return: The Nx2 concentration matrix, where N = H * W is number of pixels.
        """
        OD = convert_RGB_to_OD(I).reshape((-1, 3))  # convert to optical density and flatten to (H*W)x3.
        return spams.lasso(OD.T, D=stain_matrix.T, mode=2, lambda1=lamda, pos=True).toarray().T
