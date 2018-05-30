from __future__ import division

from .normalizer_abc import FancyNormalizer
from ..utils import misc as mu
import numpy as np


class MacenkoNormalizer(FancyNormalizer):
    """
    Stain normalization based on the method of:
    M. Macenko et al., ‘A method for normalizing histology slides for quantitative analysis’, in 2009 IEEE International Symposium on Biomedical Imaging: From Nano to Macro, 2009, pp. 1107–1110.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_concentrations = None

    def fit(self, target):
        """
        Fit to a target image.

        :param target: Image RGB uint8.
        :return:
        """
        if self.standardize:
            target = mu.standardize_brightness(target)
        self.stain_matrix_target = self.get_stain_matrix(target)
        self.target_concentrations = self.get_concentrations(target, self.stain_matrix_target)

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
        maxC_source = np.percentile(source_concentrations, 99, axis=0).reshape((1, 2))
        maxC_target = np.percentile(self.target_concentrations, 99, axis=0).reshape((1, 2))
        source_concentrations *= (maxC_target / maxC_source)
        return (255 * np.exp(-1 * np.dot(source_concentrations, self.stain_matrix_target).reshape(I.shape))).astype(
            np.uint8)

    @staticmethod
    def get_stain_matrix(I, beta=0.15, alpha=1):
        """
        Get the stain matrix (2x3). First row H and second row E.
        See the original paper for details.

        :param I: Image RGB uint8.
        :param beta:
        :param alpha:
        :return:
        """
        OD = mu.RGB_to_OD(I).reshape((-1, 3))
        OD = (OD[(OD > beta).any(axis=1), :])
        _, V = np.linalg.eigh(np.cov(OD, rowvar=False))
        V = V[:, [2, 1]]
        if V[0, 0] < 0: V[:, 0] *= -1
        if V[0, 1] < 0: V[:, 1] *= -1
        That = np.dot(OD, V)
        phi = np.arctan2(That[:, 1], That[:, 0])
        minPhi = np.percentile(phi, alpha)
        maxPhi = np.percentile(phi, 100 - alpha)
        v1 = np.dot(V, np.array([np.cos(minPhi), np.sin(minPhi)]))
        v2 = np.dot(V, np.array([np.cos(maxPhi), np.sin(maxPhi)]))
        if v1[0] > v2[0]:
            HE = np.array([v1, v2])
        else:
            HE = np.array([v2, v1])
        return mu.normalize_rows(HE)
