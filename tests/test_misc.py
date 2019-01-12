import numpy as np

from staintools.tissue_masks.luminosity_threshold_tissue_locator import LuminosityThresholdTissueLocator
from staintools.miscellaneous.exceptions import TissueMaskException
from staintools.preprocessing.input_validation import is_uint8_image
from staintools.miscellaneous.miscellaneous_functions import normalize_matrix_rows


def test_normalize_matrix_rows():
    x = np.array([[1, 1, 1],
                  [1, 0, 1]])
    r2, r3 = np.sqrt(1 / 2), np.sqrt(1 / 3)
    xnorm = np.array([[r3, r3, r3],
                      [r2, 0, r2]])
    assert np.allclose(xnorm, normalize_matrix_rows(x))


def test_is_uint8_image():
    R = np.array([[0., 55., 250.],
                  [1., 3., 7.],
                  [2., 4., 7.]])
    G = np.array([[0., 55., 250.],
                  [1., 3., 7.],
                  [2., 4., 7.]])
    B = np.array([[0., 55., 250.],
                  [1., 3., 7.],
                  [2., 4., 7.]])

    I = np.array([R, G, B])
    assert not is_uint8_image(I)
    I = I.astype(np.uint8)
    assert is_uint8_image(I)
    I = I / 255
    assert not is_uint8_image(I)


def test_tissue_mask_for_white_image():
    x = np.zeros(shape=(100, 100, 3), dtype=np.uint8)
    x[:] = 255

    raises = False
    try:
        LuminosityThresholdTissueLocator.get_tissue_mask(x, 0.8)
    except TissueMaskException:
        raises = True
    assert raises

