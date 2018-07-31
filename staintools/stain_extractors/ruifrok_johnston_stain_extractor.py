from __future__ import division

import numpy as np

from staintools.stain_extractors.abc_stain_extractor import StainExtractor


class RuifrokJohnstonStainExtractor(StainExtractor):

    @staticmethod
    def get_stain_matrix(I):
        """
        Get Ruifrok-Johnston stain matrix.

        :return:
        """
        stain_matrix = np.array(
            [
                [+0.644, +0.716, +0.266],
                [+0.092, +0.954, +0.283],
                [-0.090, -0.275, +0.957]
            ]
        )
        return stain_matrix
