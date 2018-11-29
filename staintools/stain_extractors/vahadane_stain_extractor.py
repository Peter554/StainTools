from __future__ import division

import spams

from staintools.stain_extractors.abc_stain_extractor import StainExtractor
from staintools.utils.misc_utils import convert_RGB_to_OD, normalize_rows, get_tissue_mask

class VahadaneStainExtractor(StainExtractor):

    @staticmethod
    def get_stain_matrix(I, luminosity_threshold=0.8, dictionary_regularizer=0.1):
        """
        Stain matrix estimation via method of:
        A. Vahadane et al.,
        'Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images'

        :param I: Image RGB uint8.
        :param luminosity_threshold:
        :param dictionary_regularizer:
        :return:
        """
        # convert to OD and ignore background
        tissue_mask = get_tissue_mask(I, luminosity_threshold=luminosity_threshold).reshape((-1,))
        OD = convert_RGB_to_OD(I).reshape((-1, 3))
        OD = OD[tissue_mask]

        # do the dictionary learning
        dictionary = spams.trainDL(X=OD.T, K=2, lambda1=dictionary_regularizer, mode=2,
                                   modeD=0, posAlpha=True, posD=True, verbose=False).T

        # order H and E.
        # H on first row.
        if dictionary[0, 0] < dictionary[1, 0]:
            dictionary = dictionary[[1, 0], :]

        return normalize_rows(dictionary)
