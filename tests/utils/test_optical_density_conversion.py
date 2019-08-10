import sys
import unittest
from unittest.mock import Mock
import numpy as np

sys.modules['spams'] = Mock()

from staintools.utils.optical_density_conversion import convert_RGB_to_OD, convert_OD_to_RGB


class TestOpticalDensityConversion(unittest.TestCase):
    def test_convert_RGB_to_OD(self):
        rgb = np.random.randint(0, 256, [7, 2, 3])

        get = convert_RGB_to_OD(rgb)

        for i in range(3):
            for j in range(2):
                for k in range(3):
                    expect = -1 * np.log(rgb[i, j, k] / 255)
                    self.assertAlmostEqual(expect, get[i, j, k])

    def test_convert_OD_to_RGB(self):
        od = np.random.uniform(0, 1, [4, 5, 3])

        get = convert_OD_to_RGB(od)

        for i in range(3):
            for j in range(2):
                for k in range(3):
                    expect = (255 * np.exp(-1 * od[i, j, k])).astype(np.uint8)
                    self.assertAlmostEqual(expect, get[i, j, k])
