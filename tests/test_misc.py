import os
from pathlib import Path
import numpy as np

import staintools
from staintools.stain_extractors.vahadane_stain_extractor import VahadaneStainExtractor
from staintools.utils.misc_utils import *
from staintools.utils.exceptions import *


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

def test_tissue_mask_for_white_image():
    x = np.zeros(shape=(100, 100, 3), dtype=np.uint8)
    x[:] = 255

    # Ensure the proper exception is raised
    try:
        get_tissue_mask(x, 0.8)
    except TissueMaskException as e:
        print(e)
        assert True
        return
    assert False

def test_vahadane_stain_extractor_for_white_image():
    x = np.zeros(shape=(100, 100, 3), dtype=np.uint8)
    x[:] = 255

    # Ensure the proper exception is raised
    try:
        VahadaneStainExtractor.get_stain_matrix(x)
    except TissueMaskException as e:
        print(e)
        assert True
        return
    assert False
