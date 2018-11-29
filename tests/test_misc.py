import os
from pathlib import Path
import staintools
from staintools.stain_extractors.vahadane_stain_extractor import VahadaneStainExtractor, VahadaneStainExtractorException
from staintools.utils.misc_utils import *
import numpy as np


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


def test_vahadane_stain_extractor():
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    i1 = staintools.read_image(str(script_dir / ".." / "data" / "i1.png"))
    x = np.zeros(shape=i1.shape, dtype=np.uint8)
    x[:] = 255

    # Ensure the proper exception is raised
    try:
        VahadaneStainExtractor.get_stain_matrix(x)
    except VahadaneStainExtractorException as e:
        print(e)
        assert True
        return
    assert False
