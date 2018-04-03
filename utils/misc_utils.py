"""
Other utilities
"""

from __future__ import division

import numpy as np
import cv2 as cv


def standardize_brightness(I):
    """
    An image is a numpy array of size HxWx3 (RGB) with integer values in the range 0-255 (uint8).
    We standardize so 10% of the elements of this array take the value 255.
    For already bright images this makes little change. For dark images this makes a significant difference,
    :param I:
    :return:
    """
    p = np.percentile(I, 90)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)


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
