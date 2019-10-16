import numpy as np
import copy

from staintools.stain_extraction.macenko_stain_extractor import MacenkoStainExtractor
from staintools.stain_extraction.vahadane_stain_extractor import VahadaneStainExtractor
from staintools.tissue_masks.luminosity_threshold_tissue_locator import LuminosityThresholdTissueLocator
from staintools.utils.get_concentrations import get_concentrations


class StainAugmentor(object):

    def __init__(self, method, sigma1=0.2, sigma2=0.2, augment_background=True):
        if method.lower() == 'macenko':
            self.extractor = MacenkoStainExtractor
        elif method.lower() == 'vahadane':
            self.extractor = VahadaneStainExtractor
        else:
            raise Exception('Method not recognized.')
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.augment_background = augment_background

    def fit(self, I):
        """
        Fit to an image I.

        :param I:
        :return:
        """
        self.image_shape = I.shape
        self.stain_matrix = self.extractor.get_stain_matrix(I)
        self.source_concentrations = get_concentrations(I, self.stain_matrix)
        self.n_stains = self.source_concentrations.shape[1]
        self.tissue_mask = LuminosityThresholdTissueLocator.get_tissue_mask(I).ravel()

    def pop(self):
        """
        Get an augmented version of the fitted image.

        :return:
        """
        augmented_concentrations = copy.deepcopy(self.source_concentrations)

        for i in range(self.n_stains):
            alpha = np.random.uniform(1 - self.sigma1, 1 + self.sigma1)
            beta = np.random.uniform(-self.sigma2, self.sigma2)
            if self.augment_background:
                augmented_concentrations[:, i] *= alpha
                augmented_concentrations[:, i] += beta
            else:
                augmented_concentrations[self.tissue_mask, i] *= alpha
                augmented_concentrations[self.tissue_mask, i] += beta

        I_augmented = 255 * np.exp(-1 * np.dot(augmented_concentrations, self.stain_matrix))
        I_augmented = I_augmented.reshape(self.image_shape)
        I_augmented = np.clip(I_augmented, 0, 255)

        return I_augmented
