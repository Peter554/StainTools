from __future__ import division

import spams

from staintools.normalization.normalizer_abc import StainNormalizer
from staintools.utils.misc import get_nonwhite_mask, convert_RGB_to_OD, normalize_rows


class VahadaneNormalizer(StainNormalizer):
    """
    Stain normalization inspired by method of:
    A. Vahadane et al., ‘Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images’, IEEE Transactions on Medical Imaging, vol. 35, no. 8, pp. 1962–1971, Aug. 2016.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_stain_matrix(I, threshold=0.8, lamda=0.1):
        """
        Get the 2x3 stain matrix. First row H and second row E.
        See the original paper for details.
        Also see spams docs.

        :param I: Image RGB uint8.
        :param threshold:
        :param lamda:
        :return:
        """
        mask = get_nonwhite_mask(I, thresh=threshold).reshape((-1,))
        OD = convert_RGB_to_OD(I).reshape((-1, 3))
        OD = OD[mask]  # ignore background
        dictionary = spams.trainDL(OD.T, K=2, lambda1=lamda, mode=2, modeD=0, posAlpha=True, posD=True, verbose=False).T
        if dictionary[0, 0] < dictionary[1, 0]:  # order H and E - H on first row.
            dictionary = dictionary[[1, 0], :]
        return normalize_rows(dictionary)
