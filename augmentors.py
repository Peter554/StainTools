"""
Augmentors objects
"""
import numpy as np
from utils import misc_utils as mu

def RJ_concentrations(I):
    """
    Performs stain concentartion extraction according to
    A. C. Ruifrok, D. A. Johnston et al., “Quantification of histochemical
    staining by color deconvolution,” Analytical and quantitative cytology
    and histology, vol. 23, no. 4, pp. 291–299, 2001.
    """
    OD = mu.RGB_to_OD(I).reshape((-1, 3))

    stain_matrix = np.array([[0.644211, 0.716556, 0.266844],
          [0.092789, 0.954111, 0.283111],
          [-0.0903,-0.2752, 0.9571]])

    source_concentrations = np.dot(OD, np.linalg.inv(stain_matrix))

    return source_concentrations, stain_matrix

class Fancy_concentrations(object):
    """
    Performs stain concentration exctraction according to
    Macenko or Vahadane
    :param method; type normalizers object
    :return: concentration (Npix x 2)
    """
    def __init__(self, method):
        self.method = method

    def compute(self, I, just_stain=False):
        """
        By default returns stain_matrix and concentrations
        To compute just stain_matrix set just_stain to True
        """
        stain_matrix = self.method.get_stain_matrix(I)
        if just_stain == True:
            return stain_matrix
        else:
            source_concentrations = self.method.get_concentrations(I, stain_matrix)
            return source_concentrations, stain_matrix

def assign_method(method):
    """
    Tests and returns augmentation method
    """
    assert method in ['RJ', 'Macenko', 'Vahadane'], 'select appropriate method!'

    if method == 'RJ':
        return RJ_concentrations
    if method == 'Macenko':
        from normalizers import MacenkoNormalizer
        return Fancy_concentrations(MacenkoNormalizer).compute
    if method == 'Vahadane':
        from normalizers import VahadaneNormalizer
        return Fancy_concentrations(VahadaneNormalizer).compute

class Augmentor(object):
    """
    Augment a patch or a directory with patches according to method
    described in:
    Tellez, D., M. Balkenhol, I. Otte-Höller, R. van de Loo, R. Vogels, P. Bult,
    C. Wauters, et al. “Whole-Slide Mitosis Detection in H #x0026;E Breast Histology
    Using PHH3 as a Reference to Train Distilled Stain-Invariant Convolutional Networks.”
    IEEE Transactions on Medical Imaging PP, no. 99 (2018): 1–1.
    """

    def __init__(self, method='RJ', sigma1=0.3, sigma2=0.3):
        """
        Initialise by specifying which stain matrix and source estimation method to use
        :param stain_matrix_method: type str; 'RJ' 'Macenko' 'Vahadane'
        """

        self.method = assign_method(method)
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def augment(self, I, new_stain_mat=False):
        """
        Get concentrations and return augmented image
        :param I; image to be augmented
        :param new_stain_mat; type bool, if True computes & returns new stain matrix
        """
        source_concentrations, stain_matrix = self.method(I)

        iter = source_concentrations.shape[1]
        for i in range(iter):
            alpha = np.random.uniform(1-self.sigma1, 1+self.sigma1)
            beta = np.random.uniform(-self.sigma2, self.sigma2)
            source_concentrations[:,i] *= alpha
            source_concentrations[:,i] += beta

        I_prime = np.clip((255 * np.exp(-1 * np.dot(source_concentrations, stain_matrix).reshape(I.shape))), 0, 255).astype(
            np.uint8)

        if new_stain_mat:
            stain_matrix = self.method(I, just_stain=True)
            return I_prime, stain_matrix
        else:
            return I_prime

if __name__ == '__main__':
    import cv2
    import matplotlib.pyplot as plt
    from utils.visual_utils import read_image
    I = read_image('data/i1.png')
    # Test 1
    for method in ['RJ', 'Macenko', 'Vahadane', 'test']:
        try:
            augmentor = Augmentor(method=method)
            I_prime = augmentor.augment(I)
            f, axarr = plt.subplots(1,2)
            axarr[0].imshow(I)
            axarr[1].imshow(I_prime)
            plt.show()
        except AssertionError:
            print('Cought faulty method, YAY!')
    # Tets 2
    for method in ['Macenko', 'Vahadane']:
        augmentor = Augmentor(method=method)
        I_prime, stain_matrix = augmentor.augment(I, new_stain_mat=True)
