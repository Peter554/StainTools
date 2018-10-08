StainTools
==========

Tools for tissue image stain normalization and augmentation in Python (tested on 3.5).

.. image:: https://i.imgur.com/sS8AKaV.png
    :width: 95%
.. image:: https://i.imgur.com/PzY0fE7.png
    :width: 95%

Install
========

``pip install staintools`` + install SPAMS (see below)

StainTools requires the SPAMS (SPArse Modeling Software) package. Please find out about this `here <http://spams-devel.gforge.inria.fr>`__. This may be installed via conda. For example, see `here <https://github.com/conda-forge/python-spams-feedstock>`__. Alternatively, a version is currently available from the PyPI testing site - run ``pip install --index-url https://test.pypi.org/simple/ spams``. Hopefully, SPAMS will soon be available on the main PyPI.

Docs
====

Histology images are often stained with the Hematoxylin & Eosin (H&E) stains. These two chemicals typically stain: the nuclei a dark purple (Hematoxylin) and the cytoplasm a light pink (Eosin). Thus all pixels in a histology image are principally composed of two colors. These stain colors vary from image to image and may be summarised in a stain matrix:

.. math::
    S = \left(
    \begin{array}{ccc}
    H_R & H_G & H_B \\
    E_R & E_G & E_B
    \end{array}
    \right)

The first row of this matrix shows the Hematoxylin stain color in RGB. The second row of the matrix shows the Eosin stain color in RGB. Strictly speaking these RGB values should be interpreted in optical density space. We transform a normal RGB image to a RGB optical density image via the Beer-Lambert Law:

.. math::
    I = 255 \times \exp(-OD)

If we flatten the OD image so that it is Npix x 3, with Npix = h x w and h and w the original image height and width, then we can relate the OD array and the stain matrix via the pixel concentration matrix C (a Npix x 2 array where the columns give the pixel concentration of H and E respectively):

.. math::
    OD_{flat} = C S

A :code:`StainExtractor` provides methods for estimating a stain matrix and a concentration matrix given an image. We implement:

- :code:`MacenkoStainExtractor`. Stain matrix estimation via method of *M. Macenko et al.,“A method for normalizing histology slides for quantitative analysis,”*. This method considers the projection of pixels onto the 2D plane defined by the two principle eigenvectors of the optical density covariance matrix. It then considers the extreme directions (in terms of angular polar coordinate) in this plane. See the paper for details.

- :code:`VahadaneStainExtractor`. Stain matrix estimation via method of *A. Vahadane et al., “Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images,”*. This method takes a dictionary learning based approach to find the two basis stains that best fit the image. See the paper for details.

In both cases the first step is to attempt to remove background pixels - pixels of the image where no tissue was present. In principle these should be just white light therefore we isolate tissue by a thresholding on the pixel luminosity. For some images that are dimly lit however the background is not bright enough and therefore it is recommended to standardize the brightness of any image first. For this we implement a :code:`BrightnessStandardizer`, which enforces an image to have at least 5% of pixels being luminosity saturated.
To understand this better it is recommended to see the demo notebook `demo_brightness_standardizer_and_luminosity_mask <https://github.com/Peter554/StainTools/blob/master/demo_brightness_standardizer_and_luminosity_mask.ipynb>`__.

Once we have the stain and concentration matrices we are able to easily carry out.

- **Stain Normalization**. This basically involves casting one image in the stain colors of a target image. For this we basically decompose the images into the stain matrix S and the concentration matrix C, then replace the stain matrix of the image to be transformed with that of the target image. We then recombine to give the final stain normalized image. This is implemented in the class :code:`StainNormalizer`. See the demo notebook `demo_stain_normalizer <https://github.com/Peter554/StainTools/blob/master/demo_stain_normalizer.ipynb>`__ for an example.

- **Stain Augmentation**. For this we simply augment a single image by decomposing it into the stain matrix S and the concentration matrix C, perturbing the concentrations somewhat and then recombining to be get an augmented image. This is implemented in the class :code:`StainAugmentor`. See the demo notebook `demo_stain_augmentor <https://github.com/Peter554/StainTools/blob/master/demo_stain_augmentor.ipynb>`__ for an example.

We also implement a simpler color normalizer, the :code:`ReinhardColorNormalizer`, which normalizes images according to the method of *E. Reinhard, M. Adhikhmin, B. Gooch, and P. Shirley, ‘Color transfer between images’*. This method does not consider the details of stain matrices etc. Instead it simply maps the color distribution mean and standard deviation to match that of another target image. See the demo notebook `demo_reinhard_color_normalizer <https://github.com/Peter554/StainTools/blob/master/demo_reinhard_color_normalizer.ipynb>`__ for an example.

