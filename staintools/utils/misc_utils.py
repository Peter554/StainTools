"""
Miscellaneous utilities.
"""

from __future__ import division

import numpy as np
import cv2 as cv

from staintools.utils.exceptions import *

def remove_zeros(I):
    """
    Remove zeros in an image, replace with 1's.

    :param I: An Array.
    :return: New array where 0's have been replaced with 1's.
    """
    mask = (I == 0)
    I[mask] = 1
    return I


def convert_RGB_to_OD(I):
    """
    Convert from RGB to optical density (OD_RGB) space.

    RGB = 255 * exp(-1*OD_RGB).

    :param I: Image RGB uint8.
    :return: Optical denisty RGB image.
    """
    I = remove_zeros(I)  # we don't want to take the log of zero.
    return -1 * np.log(I / 255)


def convert_OD_to_RGB(OD):
    """
    Convert from optical density (OD_RGB) to RGB.

    RGB = 255 * exp(-1*OD_RGB)

    :param OD: Optical denisty RGB image.
    :return: Image RGB uint8.
    """
    assert OD.min() >= 0, "Negative optical density."
    return (255 * np.exp(-1 * OD)).astype(np.uint8)


def normalize_rows(A):
    """
    Normalize the rows of an array.

    :param A: An array.
    :return: Array with rows normalized.
    """
    return A / np.linalg.norm(A, axis=1)[:, None]


def get_tissue_mask(I, luminosity_threshold=0.8):
    """
    Get a binary mask where true denotes pixels with a luminosity less than the specified threshold.
    Typically we use to identify tissue in the image and exclude the bright white background.

    :param I: RGB uint 8 image.
    :param luminosity_threshold: Luminosity threshold.
    :return: Binary mask.
    """
    assert is_uint8_image(I), "Image should be RGB uint8."
    I_LAB = cv.cvtColor(I, cv.COLOR_RGB2LAB)
    L = I_LAB[:, :, 0] / 255.0  # Convert to range [0,1].
    mask = L < luminosity_threshold

    # Check it's not empty
    if mask.sum() == 0:
        raise TissueMaskException("Empty tissue mask computed")

    return mask


def get_sign(x):
    """
    Returns the sign of x.

    :param x: A scalar x.
    :return: The sign of x  \in (+1, -1, 0).
    """
    if x > 0:
        return +1
    elif x < 0:
        return -1
    elif x == 0:
        return 0


def array_equal(A, B, eps=1e-5):
    """
    Are arrays A and B equal?

    :param A: Array.
    :param B: Array.
    :param eps: Tolerance.
    :return: True/False.
    """
    if A.ndim != B.ndim:
        return False
    if A.shape != B.shape:
        return False
    if np.min(np.abs(A - B)) > eps:
        return False
    return True


def is_image(x):
    """
    Is x an image?
    i.e. numpy array of 2 or 3 dimensions.

    :param x: Input.
    :return: True/False.
    """
    if not isinstance(x, np.ndarray):
        return False
    if x.ndim not in [2, 3]:
        return False
    return True


def is_gray_image(x):
    """
    Is x a gray image?

    :param x: Input.
    :return: True/False.
    """
    if not is_image(x):
        return False
    squeezed = x.squeeze()
    if not squeezed.ndim == 2:
        return False
    return True


def is_uint8_image(x):
    """
    Is x a uint8 image?

    :param x: Input.
    :return: True/False.
    """
    if not is_image(x):
        return False
    if x.dtype != np.uint8:
        return False
    return True


def check_image_and_squeeze_if_gray(I):
    """
    Check that I is an image and squeeze to 2D if it is gray.

    :param I:
    :return:
    """
    assert is_image(I), "Should be an image (2 or 3D numpy array)."
    if is_gray_image(I):
        return I.squeeze()
    else:
        return I
