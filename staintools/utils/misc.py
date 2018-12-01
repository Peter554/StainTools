"""
Miscellaneous utilities.
"""

import numpy as np


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


