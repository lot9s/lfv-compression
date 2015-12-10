import numpy as np
from scipy.fftpack import dct, idct

def transform(array):
    """
    Args:
        list(list(numpy.ndarray)): 2D list of uint8 numpy arrays
    Returns:
        list(list(numpy.ndarry)): the dct coefficients as float32 of each numpy array in the 2D list
    """
    return [
        [dct(array[x][y].astype(np.float32), norm='ortho')
         for y in range(0, len(array[x]))]
         for x in range(0, len(array))
    ]

def inverse_transform(array):
    """
    Args:
        list(list(numpy.ndarray)): 2D list of numpy array dct coefficients as float32 of each numpy array
    Returns:
        list(list(numpy.ndarry)): the idct casted to uint8 of each numpy array in the 2D list
    """
    return [
        [np.rint(idct(array[x][y], norm='ortho')).astype(np.int16)
         for y in range(0, len(array[x]))]
         for x in range(0, len(array))
    ]
