"""
Visualization utilities.
"""

from __future__ import division

import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

from . import misc as mu


###

def read_image(path):
    """
    Read an image to RGB uint8.
    Read with opencv (cv) and covert from BGR colorspace to RGB.

    :param path: The path to the image.
    :return: RGB uint8 image.
    """
    assert os.path.isfile(path), 'File not found'
    im = cv.imread(path)
    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    return im


def show_colors(C):
    """
    Visualize rows of C as colors (RGB)

    :param C: An array N x 3 where the rows are considered as RGB colors.
    :return:
    """
    assert isinstance(C, np.ndarray)
    assert C.ndim == 2
    assert C.shape[1] == 3
    n = C.shape[0]
    range255 = C.max() > 1.0
    for i in range(n):
        if range255:
            plt.plot([0, 1], [n - 1 - i, n - 1 - i], c=C[i] / 255, linewidth=20)
        else:
            plt.plot([0, 1], [n - 1 - i, n - 1 - i], c=C[i], linewidth=20)
        plt.axis('off')
        plt.axis([0, 1, -1, n])


def show(image, now=True, fig_size=(10, 10)):
    """
    Show an image (np.array).
    Caution! Rescales image to be in range [0,1].

    :param image:
    :param now: plt.show() now?
    :param fig_size: Figure size.
    :return:
    """
    image = mu.check_image(image)
    is_gray = True if image.ndim == 2 else False
    image = image.astype(np.float32)
    m, M = image.min(), image.max()
    if fig_size != None:
        plt.rcParams['figure.figsize'] = (fig_size[0], fig_size[1])
    if is_gray:
        plt.imshow((image - m) / (M - m), cmap='gray')
    else:
        plt.imshow((image - m) / (M - m))
    plt.axis('off')
    if now == True:
        plt.show()


def build_stack(images):
    """
    Build a stack of images from a tuple/list of images.

    :param images: A tuple/list of images.
    :return:
    """
    N = len(images)
    images = [mu.check_image(image) for image in images]
    for image in images:
        assert image.ndim == images[0].ndim
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


def patch_grid(ims, width=5, sub_sample=False, rand=False, save_name=None):
    """
    Display a grid of patches.

    :param ims: A patch 'stack'
    :param width: Images per row.
    :param sub_sample: Should we take a subsample?
    :param rand: Randomize subsample?
    :return:
    """
    N0 = np.shape(ims)[0]
    if sub_sample and rand:
        N = sub_sample
        idx = np.random.choice(range(N), sub_sample, replace=False)
        stack = ims[idx]
    elif sub_sample and not rand:
        N = sub_sample
        stack = ims[:N]
    else:
        N = N0
        stack = ims
    height = np.ceil(float(N) / width).astype(np.uint16)
    plt.rcParams['figure.figsize'] = (18, (18 / width) * height)
    plt.figure()
    for i in range(N):
        plt.subplot(height, width, i + 1)
        show(stack[i], now=False, fig_size=None)
    if save_name != None:
        os.makedirs(os.path.dirname(save_name), exist_ok=True)
        plt.savefig(save_name)
    plt.show()

