from staintools.utils.misc import *
import numpy as np


def test_normalize_rows():
    x = np.array([[1, 1, 1],
                  [1, 0, 1]])
    r2, r3 = np.sqrt(1 / 2), np.sqrt(1 / 3)
    xnorm = np.array([[r3, r3, r3],
                      [r2, 0, r2]])
    assert array_equal(xnorm, normalize_rows(x))


def test_is_uint8_image():
    x = np.array([[0., 55., 250.],
                  [1., 3., 7.],
                  [2., 4., 7.]])
    assert not is_uint8_image(x)
    x = x.astype(np.uint8)
    assert is_uint8_image(x)
    x = x / 255
    assert not is_uint8_image(x)


