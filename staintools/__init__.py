import sys
if sys.version_info[0] < 3:
    raise Exception("Error: You are not running Python 3.")

from staintools.stain_extractors.vahadane_stain_extractor import VahadaneStainExtractor
from staintools.stain_extractors.macenko_stain_extractor import MacenkoStainExtractor

from staintools.stain_normalizer import StainNormalizer
from staintools.stain_augmentor import StainAugmentor

from staintools.reinhard_color_normalizer import ReinhardColorNormalizer

from staintools.utils.brightness_standardizer import BrightnessStandardizer
from staintools.utils.tissue_mask import get_tissue_mask
from staintools.utils.visualization import *
