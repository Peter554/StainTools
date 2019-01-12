import numpy as np
import os
import matplotlib.pyplot as plt


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


def plot_image(image, show=True, fig_size=10, title=None):
    """
    Plot an image (np.array).
    Caution: Rescales image to be in range [0,1].

    :param image: RGB uint8
    :param show: plt.show() now?
    :param fig_size: Size of largest dimension
    :param title: Image title
    :return:
    """
    image = image.astype(np.float32)
    m, M = image.min(), image.max()
    if fig_size is not None:
        plt.rcParams['figure.figsize'] = (fig_size, fig_size)
    else:
        plt.imshow((image - m) / (M - m))
    if title is not None:
        plt.title(title)
    plt.axis("off")
    if show:
        plt.show()


def plot_image_list(images, width=5, sub_sample=False, rand=False, save_name=None, title_list=None, show=True):
    """
    Display a grid of images.

    :param images: List of RGB uint8
    :param width: Number of images per row.
    :param sub_sample: Number of images to subsample or false.
    :param rand: Should the subsample be randomized?
    :param save_name: File name to save to.
    :param title_list: A list of titles. Should only be used when sub_sample is false.
    :param show: plt.show() now?
    :return:
    """
    if sub_sample and rand:
        indicies = list(np.random.choice(range(len(images)), sub_sample, replace=False))
    elif sub_sample and not rand:
        indicies = range(sub_sample)
    else:
        indicies = range(len(images))

    height = np.ceil(float(len(indicies)) / width).astype(int)
    plt.rcParams['figure.figsize'] = (18, (18 / width) * height)
    plt.figure()

    for i in range(len(indicies)):
        plt.subplot(height, width, i + 1)
        if title_list is not None:
            plt.title(title_list[i])
        plot_image(images[i], show=False, fig_size=None)

    if save_name is not None:
        os.makedirs(os.path.dirname(save_name), exist_ok=True)
        plt.savefig(save_name)

    if show:
        plt.show()
