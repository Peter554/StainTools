import sys
import unittest
from unittest.mock import Mock
import numpy as np

sys.modules['spams'] = Mock()

from staintools.tissue_masks.luminosity_threshold_tissue_locator import LuminosityThresholdTissueLocator
from staintools.utils.exceptions import TissueMaskException


class TestLuminosityThresholdTissueLocator(unittest.TestCase):
    def test_will_locate_tissue(self):
        image = np.zeros(shape=(2, 2, 3), dtype=np.uint8)

        image[:, :, 0] = [
            [21, 247],
            [32, 250]
        ]

        image[:, :, 1] = [
            [11, 240],
            [21, 239]
        ]

        image[:, :, 2] = [
            [27, 250],
            [29, 255]
        ]

        get = LuminosityThresholdTissueLocator.get_tissue_mask(image)

        expect = np.array([
            [True, False],
            [True, False]
        ])

        self.assertTrue(np.allclose(expect, get))

    def test_throws_exception_for_white_image(self):
        image = np.ones(shape=(5, 7, 3), dtype=np.uint8) * 255

        raises = False

        try:
            LuminosityThresholdTissueLocator.get_tissue_mask(image)
        except TissueMaskException:
            raises = True

        self.assertTrue(raises)
