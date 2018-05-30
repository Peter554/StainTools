"""
Normalizer abstract base classes
"""

from __future__ import division

from abc import ABC, abstractmethod
from ..utils import misc as mu
import spams
import numpy as np


class Normaliser(ABC):
    """
    Abstract base class for normalizers. Defines some necessary methods to be considered a normalizer.
    """

    def __init__(self, **kwargs):
        self.standardize = kwargs['standardize'] if 'standardize' in kwargs.keys() else True
        if self.standardize:
            print('Using brightness standardization')
        else:
            print('Not standardizing brightness')

    @abstractmethod
    def fit(self, target):
        """Fit the normalizer to an target image"""

    @abstractmethod
    def transform(self, I):
        """Transform an image to the target stain"""


class FancyNormalizer(Normaliser):
    """
    Abstract class for a 'fancy' normalizer (inherits from Normalizer). Adds methods for stain matrix and source concentration estimation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stain_matrix_target = None

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

        :param I: Image. A np array HxWx3 of type uint8.
        :param stain_matrix: a 2x3 stain matrix. First row is Hematoxylin stain vector, second row is Eosin stain vector.
        :return: The Nx2 concentration matrix, where N=H*W is number of pixels.
        """
        OD = mu.RGB_to_OD(I).reshape((-1, 3))  # convert to optical density and flatten to (H*W)x3.
        return spams.lasso(OD.T, D=stain_matrix.T, mode=2, lambda1=lamda, pos=True).toarray().T

    def fit(self, target):
        """
        Fit to a target image.

        :param target: Target image RGB uint8.
        :return:
        """
        if self.standardize:
            target = mu.standardize_brightness(target)
        self.stain_matrix_target = self.get_stain_matrix(target)

    def transform(self, I):
        """
        Transform an image.

        :param I: Image RGB uint8.
        :return:
        """
        if self.standardize:
            I = mu.standardize_brightness(I)
        stain_matrix_source = self.get_stain_matrix(I)
        source_concentrations = self.get_concentrations(I, stain_matrix_source)
        assert stain_matrix_source.min() >= 0
        assert source_concentrations.min() >= 0
        return (255 * np.exp(-1 * np.dot(source_concentrations, self.stain_matrix_target).reshape(I.shape))).astype(
            np.uint8)

    def fetch_target_stains(self):
        """
        Fetch the target stain matrix and convert from OD to RGB.
        Must call fit first (this builds the stain matrix).

        :return:
        """
        assert self.stain_matrix_target is not None, 'Run fit method first'
        return mu.OD_to_RGB(self.stain_matrix_target)

    def hematoxylin(self, I):
        """
        Hematoxylin channel extraction.

        :param I: Image RGB uint8.
        :return:
        """
        if self.standardize:
            I = mu.standardize_brightness(I)
        h, w, c = I.shape
        stain_matrix_source = self.get_stain_matrix(I)
        source_concentrations = self.get_concentrations(I, stain_matrix_source)
        H = source_concentrations[:, 0].reshape(h, w)
        H = np.exp(-1 * H)
        return H
