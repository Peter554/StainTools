from __future__ import division

import numpy as np

from staintools.stain_extractors.abc_stain_extractor import StainExtractor
from staintools.utils.misc_utils import convert_RGB_to_OD, normalize_rows, get_tissue_mask


class MacenkoStainExtractor(StainExtractor):

    @staticmethod
    def get_stain_matrix(I, luminosity_threshold=0.8, angular_percentile=99):
        """
        Stain matrix estimation via method of:
        M. Macenko et al.,
        'A method for normalizing histology slides for quantitative analysis'

        :param I: Image RGB uint8.
        :param luminosity_threshold:
        :param angular_percentile:
        :return:
        """
        # convert to OD and ignore background
        tissue_mask = get_tissue_mask(I, luminosity_threshold=luminosity_threshold).reshape((-1,))
        OD = convert_RGB_to_OD(I).reshape((-1, 3))
        OD = OD[tissue_mask]

        # eigenvectors of cov in OD space (orthogonal as cov symmetric)
        _, V = np.linalg.eigh(np.cov(OD, rowvar=False))
        # the two principle eigenvectors
        V = V[:, [2, 1]]
        # make sure vectors are pointing the right way
        if V[0, 0] < 0: V[:, 0] *= -1
        if V[0, 1] < 0: V[:, 1] *= -1
        # project on this basis.
        That = np.dot(OD, V)

        # angular coordinates with repect to the prinicple, orthogonal eigenvectors
        phi = np.arctan2(That[:, 1], That[:, 0])
        # min and max angles
        minPhi = np.percentile(phi, 100 - angular_percentile)
        maxPhi = np.percentile(phi, angular_percentile)

        # the two principle colors
        v1 = np.dot(V, np.array([np.cos(minPhi), np.sin(minPhi)]))
        v2 = np.dot(V, np.array([np.cos(maxPhi), np.sin(maxPhi)]))

        # order of H and E.
        # H first row.
        if v1[0] > v2[0]:
            HE = np.array([v1, v2])
        else:
            HE = np.array([v2, v1])

        return normalize_rows(HE)
