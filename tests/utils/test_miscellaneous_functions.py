import sys
import unittest
from unittest.mock import Mock
import numpy as np

sys.modules['spams'] = Mock()

from staintools.utils.miscellaneous_functions import get_sign, normalize_matrix_rows


class TestMiscellaneousFunctions(unittest.TestCase):
    def test_get_sign(self):
        for arg, expect in [(42, 1), (-10, -1), (0, 0)]:
            with self.subTest():
                get = get_sign(arg)
                self.assertEqual(expect, get)

    def test_normalize_matrix_rows(self):
        data = np.array([[1, 1, 1],
                         [1, 0, 1]])

        root2, root3 = np.sqrt(1 / 2), np.sqrt(1 / 3)

        expect = np.array([[root3, root3, root3],
                           [root2, 0, root2]])

        get = normalize_matrix_rows(data)

        self.assertTrue(np.allclose(expect, get))
