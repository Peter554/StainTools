import spams

from staintools.miscellaneous.optical_density_conversion import convert_RGB_to_OD


def get_concentrations(I, stain_matrix, **kwargs):
    """
    Estimate concentration matrix given an image and stain matrix.
    """
    OD = convert_RGB_to_OD(I).reshape((-1, 3))
    lasso_regularizer = kwargs['lasso_regularizer'] if 'lasso_regularizer' in kwargs.keys() else 0.01
    return spams.lasso(X=OD.T, D=stain_matrix.T, mode=2, lambda1=lasso_regularizer, pos=True).toarray().T
