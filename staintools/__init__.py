import sys
if sys.version_info[0] < 3:
    raise Exception("Error: You are not running Python 3.")

from staintools.stain_extraction.vahadane_stain_extractor import VahadaneStainExtractor
from staintools.stain_extraction.macenko_stain_extractor import MacenkoStainExtractor

from staintools.stain_normalizer import StainNormalizer
from staintools.stain_augmentor import StainAugmentor
from staintools.reinhard_color_normalizer import ReinhardColorNormalizer

from staintools.preprocessing.luminosity_standardizer import LuminosityStandardizer
from staintools.preprocessing.read_image import read_image
from staintools.visualization.visualization import *
