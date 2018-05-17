"""
Other utilities
"""

from __future__ import division

import numpy as np
import cv2 as cv


def standardize_brightness(I, percentile=95):
    """
    Standardize brightness
    :param I:
    :return:
    """
    assert is_uint8_image(I)
    I_LAB = cv.cvtColor(I, cv.COLOR_RGB2LAB)
    L = I_LAB[:, :, 0]
    p = np.percentile(L, percentile)
    I_LAB[:, :, 0] = np.clip(255. * L / p, 0, 255).astype(np.uint8)  # 255. float seems to be important...
    I = cv.cvtColor(I_LAB, cv.COLOR_LAB2RGB)
    return I


def remove_zeros(I):
    """
    Remove zeros in an image, replace with 1's.
    :param I: uint8 array
    :return:
    """
    mask = (I == 0)
    I[mask] = 1
    return I


def RGB_to_OD(I):
    """
    Convert from RGB to optical density (OD_RGB) space.
    RGB = 255 * exp(-1*OD_RGB)
    :param I:
    :return:
    """
    I = remove_zeros(I)  # we don't want to take the log of zero..
    return -1 * np.log(I / 255)


def OD_to_RGB(OD):
    """
    Convert from optical density (OD_RGB) to RGB
    RGB = 255 * exp(-1*OD_RGB)
    :param OD:
    :return:
    """
    assert OD.min() >= 0, 'Negative optical density'
    return (255 * np.exp(-1 * OD)).astype(np.uint8)


def normalize_rows(A):
    """
    Normalize the rows of an array.
    :param A:
    :return:
    """
    return A / np.linalg.norm(A, axis=1)[:, None]


def notwhite_mask(I, thresh=0.8):
    """
    Get a binary mask where true denotes 'not white'.
    Specifically, a pixel is not white if its luminance (in LAB color space) is less than the specified threshold.
    :param I:
    :param thresh:
    :return:
    """
    assert is_uint8_image(I)
    I_LAB = cv.cvtColor(I, cv.COLOR_RGB2LAB)
    L = I_LAB[:, :, 0] / 255.0
    return (L < thresh)


def sign(x):
    """
    Returns the sign of x.
    :param x:
    :return:
    """
    if x > 0:
        return +1
    elif x < 0:
        return -1
    elif x == 0:
        return 0


### Checks

def array_equal(A, B, eps=1e-9):
    """
    Are arrays A and B equal?
    :param A:
    :param B:
    :param eps:
    :return:
    """
    if A.ndim != B.ndim:
        return False
    if A.shape != B.shape:
        return False
    if np.mean(A - B) > eps:
        return False
    return True


def is_image(x):
    """
    Is x an image?
    i.e. numpy array of 2 or 3 dimensions.
    :param x:
    :return:
    """
    if not isinstance(x, np.ndarray):
        return False
    if x.ndim not in [2, 3]:
        return False
    return True


def is_gray_image(x):
    """
    Is x a gray image?
    :param x:
    :return:
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
    :param x:
    :return:
    """
    if not is_image(x):
        return False
    if x.dtype != np.uint8:
        return False
    return True


def check_image(x):
    """
    Check if is an image.
    If gray make sure it is 'squeezed' correctly.
    :param x:
    :return:
    """
    assert is_image(x)
    if is_gray_image(x):
        x = x.squeeze()
    return x
