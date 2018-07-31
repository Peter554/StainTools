from __future__ import division

import numpy as np

from staintools.normalization.normalizer_abc import StainNormalizer
from staintools.utils.misc import normalize_rows, convert_RGB_to_OD


class MacenkoNormalizer(StainNormalizer):
    """
    Stain normalization based on the method of:
    M. Macenko et al., ‘A method for normalizing histology slides for quantitative analysis’, in 2009 IEEE International Symposium on Biomedical Imaging: From Nano to Macro, 2009, pp. 1107–1110.
    """

    def __init__(self):
        super().__init__()

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
        OD = convert_RGB_to_OD(I).reshape((-1, 3))
        OD = (OD[(OD > beta).any(axis=1), :])  # only the darker pixels - ignore background.
        _, V = np.linalg.eigh(np.cov(OD, rowvar=False))  # eigenvectors of cov in OD space (orthogonal as cov symmetric)
        V = V[:, [2, 1]]  # the two principle eigenvectors
        if V[0, 0] < 0: V[:, 0] *= -1  # make sure vectors are pointing the right way/
        if V[0, 1] < 0: V[:, 1] *= -1
        That = np.dot(OD, V)  # project on this basis.
        phi = np.arctan2(That[:, 1], That[:, 0])
        # min and max angles
        # think polar coordinates with repect to the prinicple, orthogonal eigenvectors
        minPhi = np.percentile(phi, alpha)
        maxPhi = np.percentile(phi, 100 - alpha)
        # the two principle colors
        v1 = np.dot(V, np.array([np.cos(minPhi), np.sin(minPhi)]))
        v2 = np.dot(V, np.array([np.cos(maxPhi), np.sin(maxPhi)]))
        # order of H and E - H first row.
        if v1[0] > v2[0]:
            HE = np.array([v1, v2])
        else:
            HE = np.array([v2, v1])
        return normalize_rows(HE)
