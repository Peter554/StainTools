from __future__ import division

from .normalizer_abc import FancyNormalizer
from ..utils import misc as mu
import spams


class VahadaneNormalizer(FancyNormalizer):
    """
    Stain normalization inspired by method of:
    A. Vahadane et al., ‘Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images’, IEEE Transactions on Medical Imaging, vol. 35, no. 8, pp. 1962–1971, Aug. 2016.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_stain_matrix(I, threshold=0.8, lamda=0.1):
        """
        Get 2x3 stain matrix. First row H and second row E.
        See the original paper for details.
        Also see spams docs.

        :param I: Image RGB uint8.
        :param threshold:
        :param lamda:
        :return:
        """
        mask = mu.notwhite_mask(I, thresh=threshold).reshape((-1,))
        OD = mu.RGB_to_OD(I).reshape((-1, 3))
        OD = OD[mask]
        dictionary = spams.trainDL(OD.T, K=2, lambda1=lamda, mode=2, modeD=0, posAlpha=True, posD=True, verbose=False).T
        if dictionary[0, 0] < dictionary[1, 0]:
            dictionary = dictionary[[1, 0], :]
        dictionary = mu.normalize_rows(dictionary)
        return dictionary
