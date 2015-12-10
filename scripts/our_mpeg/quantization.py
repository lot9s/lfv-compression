import numpy as np
"""
The quantization arrays come from here
http://www.mpeg.org/MPEG/MSSG/tm5/Ch7/Ch7.html
"""

# Intra-quantization array
QINTRA = np.array([[8,16,19,22,26,27,29,34],
[16,16,22,24,27,29,34,37],
[19,22,26,27,29,34,34,38],
[22,22,26,27,29,34,37,40],
[22,26,27,29,32,35,40,48],
[26,27,29,32,35,40,48,58],
[26,27,29,34,38,46,56,69],
[27,29,35,38,46,56,69,83]])

QINTRA3 = np.array([QINTRA.T, QINTRA.T, QINTRA.T]).T

# Inter-quantization array
QINTER = np.array([[16,17,18,19,20,21,22,23],
[17,18,19,20,21,22,23,24],
[18,19,20,21,22,23,24,25],
[19,20,21,22,23,24,26,27],
[20,21,22,23,25,26,27,28],
[21,22,23,24,26,27,28,30],
[22,23,24,26,27,28,30,31],
[23,24,25,27,28,30,31,33]])

QINTER3 = np.empty([8,8,3], dtype=np.uint8)
QINTER3[:,:,0] = QINTER
QINTER3[:,:,1] = QINTER
QINTER3[:,:,2] = QINTER

def quantize_block(block, qmatrix=QINTER3):
    """
    Perform inter quantization on all three channels in a macroblock.
    Args:
        numpy.ndarray: float32 numpy arrays of shape (n,n,3) where 0 < n <= 8
    Returns:
        numpy.ndarry: int8 macroblock elementwise divided and rounded to nearest integer
    """
    return np.round(block / qmatrix[:block.shape[0],:block.shape[1],:].astype(np.float32)).astype(np.int8)#.astype(np.uint8)

def quantize(array, qmatrix=QINTER3):
    """
    Perform inter quantization on a whole frame.
    Args:
        list(list(numpy.ndarray)): 2D list of float32 numpy arrays containing DCT coefficients
    Returns:
        list(list(numpy.ndarry)): 2D list of uint8 numpy arrays containing quantized DCT coefficients
    """
    return [
        [quantize_block(array[x][y], qmatrix)
         for y in range(0, len(array[x]))]
         for x in range(0, len(array))
    ]

def dequantize_block(block, qmatrix=QINTER3):
    """
    Perform inter dequantization on all three channels in a macroblock
    Args:
        numpy.ndarray: int8 numpy arrays of shape (n,n,3) where 0 < n <= 8
    Returns:
        numpy.ndarry: float32 macroblock
    """
    return block.astype(np.float32) * qmatrix[:block.shape[0],:block.shape[1],:]

def dequantize(array, qmatrix=QINTER3):
    """
    Perform inter dequantization on a whole frame.
    Args:
        list(list(numpy.ndarray)): 2D list of uint8 numpy arrays containing quantized DCT coefficients
    Returns:
        list(list(numpy.ndarry)): 2D list of float32 numpy arrays containing dequantized DCT coefficients
    """
    return [
        [dequantize_block(array[x][y], qmatrix)
         for y in range(0, len(array[x]))]
         for x in range(0, len(array))
    ]
