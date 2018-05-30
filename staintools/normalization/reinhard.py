from __future__ import division

from .normalizer_abc import Normaliser
from ..utils import misc as mu
import numpy as np
import cv2 as cv


class ReinhardNormalizer(Normaliser):
    """
    Normalize a patch stain to the target image using the method of:
    E. Reinhard, M. Adhikhmin, B. Gooch, and P. Shirley, ‘Color transfer between images’, IEEE Computer Graphics and Applications, vol. 21, no. 5, pp. 34–41, Sep. 2001.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_means = None
        self.target_stds = None

    def fit(self, target):
        """
        Fit to a target image

        :param target: Image RGB uint8.
        :return:
        """
        if self.standardize:
            target = mu.standardize_brightness(target)
        means, stds = self.get_mean_std(target)
        self.target_means = means
        self.target_stds = stds

    def transform(self, I):
        """
        Transform an image.

        :param I: Image RGB uint8.
        :return:
        """
        if self.standardize:
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
        Convert from RGB uint8 to LAB and split into channels.

        :param I: Image RGB uint8.
        :return:
        """
        assert mu.is_uint8_image(I)
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
        Take seperate LAB channels and merge back to give RGB uint8.

        :param I1: L
        :param I2: A
        :param I3: B
        :return: Image RGB uint8.
        """
        I1 *= 2.55
        I2 += 128.0
        I3 += 128.0
        I = np.clip(cv.merge((I1, I2, I3)), 0, 255).astype(np.uint8)
        return cv.cvtColor(I, cv.COLOR_LAB2RGB)

    def get_mean_std(self, I):
        """
        Get mean and standard deviation of each channel.

        :param I: Image RGB uint8.
        :return:
        """
        I1, I2, I3 = self.lab_split(I)
        m1, sd1 = cv.meanStdDev(I1)
        m2, sd2 = cv.meanStdDev(I2)
        m3, sd3 = cv.meanStdDev(I3)
        means = m1, m2, m3
        stds = sd1, sd2, sd3
        return means, stds
