"""
RJ stain deconvolution methods
"""

from __future__ import division

from . import misc as mu
import numpy as np

class RuifrokJohnstonDeconvolution(object):
    """
    Stain deconvolution method according to:
    A. C. Ruifrok, D. A. Johnston et al., “Quantification of histochemical
    staining by color deconvolution,” Analytical and quantitative cytology
    and histology, vol. 23, no. 4, pp. 291–299, 2001.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_stain_matrix(*args):
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

    @staticmethod
    def get_concentrations(I, stain_matrix):
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
