import numpy as np

def get_sign(x):
    """
    Returns the sign of x.

    :param x: A scalar x.
    :return: The sign of x.
    """

    if x > 0:
        return +1
    elif x < 0:
        return -1
    elif x == 0:
        return 0


def normalize_matrix_rows(A):
    """
    Normalize the rows of an array.

    :param A: An array.
    :return: Array with rows normalized.
    """
    return A / np.linalg.norm(A, axis=1)[:, None]
