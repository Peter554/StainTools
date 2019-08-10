import sys
import unittest
from unittest.mock import Mock
import numpy as np

sys.modules['spams'] = Mock()

from staintools.preprocessing.input_validation import is_image, is_uint8_image


class TestInputValidation(unittest.TestCase):
    def test_is_image_is_true_for_three_dimensional_np_array(self):
        rgb = np.random.randint(0, 10, [7, 5, 3])
        get = is_image(rgb)
        self.assertTrue(get)

    def test_is_image_is_false_for_two_dimensional_np_array(self):
        rgb = np.random.randint(0, 10, [3, 5])
        get = is_image(rgb)
        self.assertFalse(get)

    def test_is_uint8_image_is_true_for_ints_in_0_255(self):
        rgb = np.random.randint(0, 256, [5, 4, 3]).astype(np.uint8)
        get = is_uint8_image(rgb)
        self.assertTrue(get)

    def test_is_uint8_image_is_false_for_ints_outside_0_255(self):
        rgb = np.random.randint(0, 300, [5, 2, 3])
        get = is_uint8_image(rgb)
        self.assertFalse(get)

    def test_is_uint8_image_is_false_for_floats(self):
        rgb = np.random.uniform(0, 256, [2, 7, 3])
        get = is_uint8_image(rgb)
        self.assertFalse(get)
