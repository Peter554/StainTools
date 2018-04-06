"""
Stain augmentation objects
"""

from __future__ import division

import numpy as np
import normalizers
from utils import misc_utils as mu
import copy


class Fetcher(object):

    def __init__(self, method):
        """
        Object to fetch stain matrix and concentrations given a method
        :param method: one of 'RJ', 'Macenko', 'Vahadane'.
        """
        assert method in ['RJ', 'Macenko', 'Vahadane'], 'select appropriate method!'
        if method == 'RJ':
            self.stain_fetcher = self.RJ_stain
            self.concentration_fetcher = self.RJ_concentrations
        else:
            if method == 'Macenko':
                normalizer = normalizers.MacenkoNormalizer
            if method == 'Vahadane':
                normalizer = normalizers.MacenkoNormalizer
            self.stain_fetcher = normalizer.get_stain_matrix
            self.concentration_fetcher = normalizer.get_concentrations

    def compute(self, I, just_stain=False):
        """
        By default returns concentrations and stain_matrix
        To compute just stain_matrix set just_stain to True
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

    @staticmethod
    def RJ_stain(*args):
        """
        Get RJ stain matrix.
        A. C. Ruifrok, D. A. Johnston et al., “Quantification of histochemical
        staining by color deconvolution,” Analytical and quantitative cytology
        and histology, vol. 23, no. 4, pp. 291–299, 2001.
        :param args: a dummy
        :return:
        """
        stain_matrix = np.array([[0.644211, 0.716556, 0.266844],
                                 [0.092789, 0.954111, 0.283111],
                                 [-0.0903, -0.2752, 0.9571]])
        return stain_matrix

    def RJ_concentrations(self, I, stain_matrix):
        """
        Performs stain concentration extraction according to
        A. C. Ruifrok, D. A. Johnston et al., “Quantification of histochemical
        staining by color deconvolution,” Analytical and quantitative cytology
        and histology, vol. 23, no. 4, pp. 291–299, 2001.
        :param I:
        :return:
        """
        OD = mu.RGB_to_OD(I).reshape((-1, 3))
        source_concentrations = np.dot(OD, np.linalg.inv(stain_matrix))
        return source_concentrations


class TellezAugmentor(object):

    def __init__(self, method='RJ', sigma1=0.2, sigma2=0.2):
        """
        Augment a patch according to method described in:
        Tellez, D., M. Balkenhol, I. Otte-Höller, R. van de Loo, R. Vogels, P. Bult,
        C. Wauters, et al. “Whole-Slide Mitosis Detection in H&E Breast Histology
        Using PHH3 as a Reference to Train Distilled Stain-Invariant Convolutional Networks.”
        IEEE Transactions on Medical Imaging PP, no. 99 (2018): 1–1.
        :param method: one of 'RJ', 'Macenko', 'Vahadane'.
        :param sigma1:
        :param sigma2:
        """
        self.fetcher = Fetcher(method)
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def fit(self, I, standardize_brightness=True):
        """
        Fit the augmentor to an image I
        :param I:
        :return:
        """
        if standardize_brightness:
            I = mu.standardize_brightness(I)
        self.Ishape = I.shape
        self.not_white = mu.notwhite_mask(I).reshape(-1)
        self.stain_matrix, self.source_concentrations = self.fetcher.compute(I)

    def augment(self, new_stain_mat=False):
        """
        Return augmented image.
        Optionally returns new stain matrix
        :param new_stain_mat; type bool, if True computes & returns new stain matrix
        """
        channels = self.source_concentrations.shape[1]
        source_concentrations = copy.deepcopy(self.source_concentrations)
        for i in range(channels):
            alpha = np.random.uniform(1 - self.sigma1, 1 + self.sigma1)
            beta = np.random.uniform(-self.sigma2, self.sigma2)
            source_concentrations[self.not_white, i] *= alpha
            source_concentrations[self.not_white, i] += beta

        I_prime = np.clip((255 * np.exp(-1 * np.dot(source_concentrations, self.stain_matrix).reshape(self.Ishape))), 0,
                          255).astype(np.uint8)

        if new_stain_mat:
            stain_matrix = self.fetcher.compute(I_prime, just_stain=True)
            return I_prime, stain_matrix
        else:
            return I_prime


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from utils import visual_utils as vu

    I = vu.read_image('data/i1.png')

    # Test 0
    augmentor = TellezAugmentor('Vahadane')
    augmentor.fit(I)
    print('Fitting done')
    h, w, c = I.shape
    stack = np.zeros([10, h, w, c])
    for i in range(10):
        stack[i] = augmentor.augment(new_stain_mat=False)
    vu.patch_grid(stack, width=5)

    # Test 1
    for method in ['Macenko', 'Vahadane']:
        augmentor = TellezAugmentor(method=method)
        augmentor.fit(I)
        I_prime, stain_matrix = augmentor.augment(new_stain_mat=True)

    # Test 2
    for method in ['RJ', 'Macenko', 'Vahadane', 'test']:
        try:
            augmentor = TellezAugmentor(method=method)
            augmentor.fit(I)
            I_prime = augmentor.augment()
            f, axarr = plt.subplots(1, 2)
            axarr[0].imshow(I)
            axarr[1].imshow(I_prime)
            plt.show()
        except AssertionError:
            print('Cought faulty method, YAY!')  # exception ends run ?
