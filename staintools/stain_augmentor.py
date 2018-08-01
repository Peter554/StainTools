from __future__ import division

import numpy as np
import copy

from staintools.stain_extractors.ruifrok_johnston_stain_extractor import RuifrokJohnstonStainExtractor
from staintools.stain_extractors.macenko_stain_extractor import MacenkoStainExtractor
from staintools.stain_extractors.vahadane_stain_extractor import VahadaneStainExtractor
from staintools.utils.misc_utils import get_luminosity_mask


class Augmentor(object):

    def __init__(self, method, sigma1, sigma2):
        if method.lower() == 'rj':
            self.extractor = RuifrokJohnstonStainExtractor
        elif method.lower() == 'macenko':
            self.extractor = MacenkoStainExtractor
        elif method.lower() == 'vahadane':
            self.extractor = VahadaneStainExtractor
        else:
            raise Exception('Method not recognized.')
        self.sigma1 = sigma1
        self.sigma2 = sigma2


def fit(self, I):
    """
    Fit the augmentor to an image I.

    :param I:
    :return:
    """
    self.Ishape = I.shape
    self.tissue_mask = get_luminosity_mask(I).ravel()
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
