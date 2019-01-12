import numpy as np


def is_image(I):
    """
    Is I an image.
    """
    if not isinstance(I, np.ndarray):
        return False
    if not I.ndim == 3:
        return False
    return True


def is_uint8_image(I):
    """
    Is I a uint8 image.
    """
    if not is_image(I):
        return False
    if I.dtype != np.uint8:
        return False
    return True
