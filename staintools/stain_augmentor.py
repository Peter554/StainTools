"""
Stain augmentation objects
"""

from __future__ import division

import numpy as np
import copy

from staintools.augmentation.rj import RuifrokJohnstonDeconvolution
from staintools.stain_normalization.macenko_normalizer import MacenkoNormalizer
from staintools.stain_normalization.vahadane_normalizer import VahadaneNormalizer
from staintools.utils.misc_utils import get_nonwhite_mask


class Fetcher(object):

    def __init__(self, method):
        """
        Object to fetch stain matrix and concentrations given a method

        :param method: one of 'RJ', 'Macenko', 'Vahadane'.
        """
        assert method in ['RJ', 'Macenko', 'Vahadane'], 'select appropriate method!'
        if method == 'RJ':
            self.stain_fetcher = RuifrokJohnstonDeconvolution.get_stain_matrix
            self.concentration_fetcher = RuifrokJohnstonDeconvolution.get_concentrations
        else:
            if method == 'Macenko':
                normalizer = MacenkoNormalizer
            if method == 'Vahadane':
                normalizer = VahadaneNormalizer
            self.stain_fetcher = normalizer.get_stain_matrix
            self.concentration_fetcher = normalizer.get_concentrations

    def compute(self, I, just_stain=False):
        """
        By default returns concentrations and stain_matrix.
        To compute just stain_matrix set just_stain to True.

        :param I:
        :param just_stain:
        :return:
        """
        stain_matrix = self.stain_fetcher(I)
        if just_stain:
            return stain_matrix
        else:
            source_concentrations = self.concentration_fetcher(I, stain_matrix)
            return stain_matrix, source_concentrations


class TellezAugmentor(object):

    def __init__(self, method='rj', sigma1=0.2, sigma2=0.2):
        """
        Augment an image according to method described in:
        Tellez, D., M. Balkenhol, I. Otte-Höller, R. van de Loo, R. Vogels, P. Bult,
        C. Wauters, et al. “Whole-Slide Mitosis Detection in H&E Breast Histology
        Using PHH3 as a Reference to Train Distilled Stain-Invariant Convolutional Networks.”

        :param method: one of 'RJ', 'Macenko', 'Vahadane'.
        :param sigma1:
        :param sigma2:
        """
        if method.lower() == 'rj':
            self.stain_matrix = np.array(
                [
                    [+0.644, +0.716, +0.266],
                    [+0.092, +0.954, +0.283],
                    [-0.090, -0.275, +0.957]
                ]
            )
            self.
        elif method.lower() == 'macenko':
            self.get_stain_matrix = MacenkoNormalizer.get_stain_matrix
            self.get_concentrations = MacenkoNormalizer.get_concentrations
        elif method.lower() == 'vahadane':
            self.get_stain_matrix = VahadaneNormalizer.get_stain_matrix
            self.get_concentrations = VahadaneNormalizer.get_concentrations
        else:
            raise Exception("Method not recognized")

        self.sigma1 = sigma1
        self.sigma2 = sigma2


def fit(self, I):
    """
    Fit the augmentor to an image I.

    :param I:
    :return:
    """
    self.Ishape = I.shape
    self.not_white = get_nonwhite_mask(I).reshape(-1)
    self.stain_matrix, self.source_concentrations = self.fetcher.compute(I)


def augment(self, new_stain_mat=False, include_background=False):
    """
    Return augmented image.
    Optionally returns new stain matrix

    :param new_stain_mat; type bool, if True computes & returns new stain matrix
    :param include_background:
    """
    channels = self.source_concentrations.shape[1]
    source_concentrations = copy.deepcopy(self.source_concentrations)

    for i in range(channels):
        alpha = np.random.uniform(1 - self.sigma1, 1 + self.sigma1)
        beta = np.random.uniform(-self.sigma2, self.sigma2)
        if include_background:
            source_concentrations[:, i] *= alpha
            source_concentrations[:, i] += beta
        else:
            source_concentrations[self.not_white, i] *= alpha
            source_concentrations[self.not_white, i] += beta

    I_prime = np.clip((255 * np.exp(-1 * np.dot(source_concentrations, self.stain_matrix).reshape(self.Ishape))), 0,
                      255).astype(np.uint8)

    if new_stain_mat:
        stain_matrix = self.fetcher.compute(I_prime, just_stain=True)
        return I_prime, stain_matrix
    else:
        return I_prime
