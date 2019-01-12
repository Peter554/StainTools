import numpy as np


def is_image(x):
    """
    Is x an image.
    """
    if not isinstance(x, np.ndarray):
        return False
    if not x.ndim == 3:
        return False
    return True


def is_uint8_image(x):
    """
    Is x a uint8 image.
    """
    if not is_image(x):
        return False
    if x.dtype != np.uint8:
        return False
    return True
