StainTools
==========

Tools for tissue image stain normalization and augmentation in Python (tested on 3.5).

Install
========

``pip install staintools``

**NOTE:** StainTools requires the SPAMS (SPArse Modeling Software) package. Please find out about this `here <http://spams-devel.gforge.inria.fr>`__. This may be installed via conda. For example, see `here <https://github.com/conda-forge/python-spams-feedstock>`__.

Docs
====

Histology images are often stained with the Hematoxylin & Eosin (H&E) stains. These two chemicals typically stain: the nuclei a dark purple (Hematoxylin) and the cytoplasm a light pink (Eosin). Thus all pixels in a histology image are principally composed of two colors. These stain colors vary from image to image and may be summarised in a stain matrix:

.. math::
    S = \left( \begin{array}{ccc}
    H_R & H_G & H_B \\
    E_R & E_G & E_B
    \end{array} \right)

The first

This package may be broken down as:

**Stain Extraction**

A stain extractor provides methods for estimating a stain matrix and a concentration matrix given an image. We implement:

- Macenko stain extractor. Stain matrix estimation via method of *M. Macenko et al.,“A method for normalizing histology slides for quantitative analysis,”*. This method considers the projection of pixels onto the 2D plane defined by the two principle eigenvectors of the optical density covariance matrix. It then considers the extreme directions (in terms of angular polar coordinate) in this plane. See the paper for details.

- Vahadane stain extractor. Stain matrix estimation via method of *A. Vahadane et al., “Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images,”*. This method takes a dictionary learning based approach to find the two basis stains that best fit the image. See the paper for details.

**Stain Normalizer**

A stain normalizer uses a stain extractor to transform one image to the staining of another target image.

For further examples of usage please see the demo notebooks (which serve also as tests by inspection).

