import numpy as np


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