"""
Visualization utilities.
"""

from __future__ import division

import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

from staintools.utils.misc_utils import check_image_and_squeeze_if_gray


###

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


def plot_row_colors(C, fig_size=6, title=None):
    """
    Plot rows of C as colors (RGB)

    :param C: An array N x 3 where the rows are considered as RGB colors.
    :return:
    """
    assert isinstance(C, np.ndarray), "C must be a numpy array."
    assert C.ndim == 2, "C must be 2D."
    assert C.shape[1] == 3, "C must have 3 columns."
    N = C.shape[0]
    range255 = C.max() > 1.0  # quick check to see if we have an image in range [0,1] or [0,255].
    plt.rcParams['figure.figsize'] = (fig_size, fig_size)
    for i in range(N):
        if range255:
            plt.plot([0, 1], [N - 1 - i, N - 1 - i], c=C[i] / 255, linewidth=20)
        else:
            plt.plot([0, 1], [N - 1 - i, N - 1 - i], c=C[i], linewidth=20)
    if title is not None:
        plt.title(title)
    plt.axis("off")
    plt.axis([0, 1, -0.5, N-0.5])


def plot_image(image, now=True, fig_size=10, title=None):
    """
    Plot an image (np.array).
    Caution: Rescales image to be in range [0,1].

    :param image:
    :param now: plt.show() now?
    :param fig_size: Size of largest dimension
    :param title: Image title
    :return:
    """
    image = check_image_and_squeeze_if_gray(image)
    is_gray = True if image.ndim == 2 else False
    image = image.astype(np.float32)
    m, M = image.min(), image.max()
    if fig_size is not None:
        plt.rcParams['figure.figsize'] = (fig_size, fig_size)
    if is_gray:
        plt.imshow((image - m) / (M - m), cmap='gray')
    else:
        plt.imshow((image - m) / (M - m))
    plt.axis("off")
    if title is not None:
        plt.title(title)
    if now:
        plt.show()


def make_image_stack(images):
    """
    Build a stack of images from a tuple/list of images.

    :param images: A tuple/list of images.
    :return:
    """
    N = len(images)
    images = [check_image_and_squeeze_if_gray(image) for image in images]
    for image in images:
        assert image.ndim == images[0].ndim  # check all images have same number of dimensions.
    is_gray = True if images[0].ndim == 2 else False
    if is_gray:
        h, w = images[0].shape
        stack = np.zeros((N, h, w))
    else:
        h, w, c = images[0].shape
        stack = np.zeros((N, h, w, c))
    for i in range(N):
        stack[i] = images[i]
    return stack


def plot_image_stack(ims, width=5, sub_sample=False, rand=False, save_name=None, title_list=None):
    """
    Display a grid of images.

    :param ims: A patch stack.
    :param width: Number of images per row.
    :param sub_sample: Number of images to subsample or false.
    :param rand: Should the subsample be randomized?
    :param save_name: File name to save to.
    :param title_list: A list of titles. Should only be used when sub_sample is false.
    :return:
    """
    N_all = np.shape(ims)[0]

    if sub_sample and rand:
        N = sub_sample
        idx = np.random.choice(range(N), sub_sample, replace=False)
        stack = ims[idx]
    elif sub_sample and not rand:
        N = sub_sample
        stack = ims[:N]
    else:
        N = N_all
        stack = ims

    height = np.ceil(float(N) / width).astype(int)
    plt.rcParams['figure.figsize'] = (18, (18 / width) * height)
    plt.figure()

    for i in range(N):
        plt.subplot(height, width, i + 1)
        if title_list is not None:
            plt.title(title_list[i])
        plot_image(stack[i], now=False, fig_size=None)

    if save_name is not None:
        os.makedirs(os.path.dirname(save_name), exist_ok=True)
        plt.savefig(save_name)

    plt.show()
