import cv2 as cv
import os

def read_image(path):
    """
    Read an image to RGB uint8.
    Read with opencv (cv) and covert from BGR colorspace to RGB.

    :param path: The path to the image.
    :return: RGB uint8 image.
    """
    assert os.path.isfile(path), "File not found"
    im = cv.imread(path)
    # Convert from cv2 standard of BGR to our convention of RGB.
    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    return im