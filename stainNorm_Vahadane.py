"""
Stain normalization inspired by method of:

A. Vahadane et al., ‘Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images’, IEEE Transactions on Medical Imaging, vol. 35, no. 8, pp. 1962–1971, Aug. 2016.

Uses the spams package:

http://spams-devel.gforge.inria.fr/index.html

Use with python via e.g https://anaconda.org/conda-forge/python-spams
"""

from __future__ import division

import spams
import numpy as np
from utils import misc_utils as mu


class Normalizer(object):
    """
    A stain normalization object
    """

    def __init__(self):
        self.stain_matrix_target = None

    def fit(self, target):
        """
        Fit to a target image
        :param target:
        :return:
        """
        target = mu.standardize_brightness(target)
        self.stain_matrix_target = self.get_stain_matrix(target)

    def target_stains(self):
        """
        Get target stains as RGB
        :return:
        """
        return mu.OD_to_RGB(self.stain_matrix_target)

    def transform(self, I):
        """
        Transform an image
        :param I:
        :return:
        """
        I = mu.standardize_brightness(I)
        stain_matrix_source = self.get_stain_matrix(I)
        source_concentrations = self.get_concentrations(I, stain_matrix_source)
        return (255 * np.exp(-1 * np.dot(source_concentrations, self.stain_matrix_target).reshape(I.shape))).astype(
            np.uint8)

    def hematoxylin(self, I):
        """
        Get hematoxylin channel
        :param I:
        :return:
        """
        I = mu.standardize_brightness(I)
        h, w, c = I.shape
        stain_matrix_source = self.get_stain_matrix(I)
        source_concentrations = self.get_concentrations(I, stain_matrix_source)
        H = source_concentrations[:, 0].reshape(h, w)
        H = np.exp(-1 * H)
        return H

    @staticmethod
    def get_stain_matrix(I, threshold=0.8, lamda=0.1):
        """
        Get 2x3 stain matrix. First row H and second row E.
        See the original paper for details.
        Also see spams docs.
        :param I:
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
        :return:
        """
        OD = mu.RGB_to_OD(I).reshape((-1, 3))  # convert to optical density and flatten to (H*W)x3.
        return spams.lasso(OD.T, D=stain_matrix.T, mode=2, lambda1=lamda, pos=True).toarray().T
