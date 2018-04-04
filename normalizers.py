"""
Normalizer objects
Uses the spams package:
http://spams-devel.gforge.inria.fr/index.html
Use with python via e.g https://anaconda.org/conda-forge/python-spams
"""

from __future__ import division

import cv2 as cv
import numpy as np
from utils import misc_utils as mu
import spams


class ReinhardNormalizer(object):
    """
    Normalize a patch stain to the target image using the method of:
    E. Reinhard, M. Adhikhmin, B. Gooch, and P. Shirley, ‘Color transfer between images’, IEEE Computer Graphics and Applications, vol. 21, no. 5, pp. 34–41, Sep. 2001.
    """

    def __init__(self):
        self.target_means = None
        self.target_stds = None

    def fit(self, target):
        """
        Fit to a target image
        :param target:
        :return:
        """
        target = mu.standardize_brightness(target)
        means, stds = self.get_mean_std(target)
        self.target_means = means
        self.target_stds = stds

    def transform(self, I):
        """
        Transform an image
        :param I:
        :return:
        """
        I = mu.standardize_brightness(I)
        I1, I2, I3 = self.lab_split(I)
        means, stds = self.get_mean_std(I)
        norm1 = ((I1 - means[0]) * (self.target_stds[0] / stds[0])) + self.target_means[0]
        norm2 = ((I2 - means[1]) * (self.target_stds[1] / stds[1])) + self.target_means[1]
        norm3 = ((I3 - means[2]) * (self.target_stds[2] / stds[2])) + self.target_means[2]
        return self.merge_back(norm1, norm2, norm3)

    @staticmethod
    def lab_split(I):
        """
        Convert from RGB uint8 to LAB and split into channels
        :param I: uint8
        :return:
        """
        I = cv.cvtColor(I, cv.COLOR_RGB2LAB)
        I = I.astype(np.float32)
        I1, I2, I3 = cv.split(I)
        I1 /= 2.55
        I2 -= 128.0
        I3 -= 128.0
        return I1, I2, I3

    @staticmethod
    def merge_back(I1, I2, I3):
        """
        Take seperate LAB channels and merge back to give RGB uint8
        :param I1:
        :param I2:
        :param I3:
        :return:
        """
        I1 *= 2.55
        I2 += 128.0
        I3 += 128.0
        I = np.clip(cv.merge((I1, I2, I3)), 0, 255).astype(np.uint8)
        return cv.cvtColor(I, cv.COLOR_LAB2RGB)

    def get_mean_std(self, I):
        """
        Get mean and standard deviation of each channel
        :param I: uint8
        :return:
        """
        I1, I2, I3 = self.lab_split(I)
        m1, sd1 = cv.meanStdDev(I1)
        m2, sd2 = cv.meanStdDev(I2)
        m3, sd3 = cv.meanStdDev(I3)
        means = m1, m2, m3
        stds = sd1, sd2, sd3
        return means, stds


class BaseNormalizer(object):

    def target_stains(self):
        """
        Get target stains as RGB
        :return:
        """
        return mu.OD_to_RGB(self.stain_matrix_target)

    def hematoxylin(self, I):
        """
        Hematoxylin channel
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


class MacenkoNormalizer(BaseNormalizer):
    """
    Stain normalization based on the method of:
    M. Macenko et al., ‘A method for normalizing histology slides for quantitative analysis’, in 2009 IEEE International Symposium on Biomedical Imaging: From Nano to Macro, 2009, pp. 1107–1110.
    """

    def __init__(self):
        self.stain_matrix_target = None
        self.target_concentrations = None

    def fit(self, target):
        """
        Fit to a target image
        :param target:
        :return:
        """
        target = mu.standardize_brightness(target)
        self.stain_matrix_target = self.get_stain_matrix(target)
        self.target_concentrations = self.get_concentrations(target, self.stain_matrix_target)

    def transform(self, I):
        """
        Transform an image
        :param I:
        :return:
        """
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
        :param I:
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


class VahadaneNormalizer(BaseNormalizer):
    """
    Stain normalization inspired by method of:
    A. Vahadane et al., ‘Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images’, IEEE Transactions on Medical Imaging, vol. 35, no. 8, pp. 1962–1971, Aug. 2016.
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
