import sys
import unittest
from unittest.mock import Mock
import numpy as np

sys.modules['spams'] = Mock()

from staintools.tissue_masks.luminosity_threshold_tissue_locator import LuminosityThresholdTissueLocator
from staintools.utils.exceptions import TissueMaskException


class TestLuminosityThresholdTissueLocator(unittest.TestCase):
    def test_throws_exception_for_white_iamge(self):
        x = np.ones(shape=(3, 3, 3), dtype=np.uint8) * 255

        raises = False

        try:
            LuminosityThresholdTissueLocator.get_tissue_mask(x)
        except TissueMaskException:
            raises = True

        self.assertTrue(raises)
