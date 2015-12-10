import numpy as np

ZIGZAGINVERSE = np.array([[0,  1,  5,  6,  14, 15, 27, 28],
                   [2,  4,  7,  13, 16, 26, 29, 42],
                   [3,  8,  12, 17, 25, 30, 41, 43],
                   [9,  11, 18, 24, 31, 40, 44,53],
                   [10, 19, 23, 32, 39, 45, 52,54],
                   [20, 22, 33, 38, 46, 51, 55,60],
                   [21, 34, 37, 47, 50, 56, 59,61],
                   [35, 36, 48, 49, 57, 58, 62,63]])

ZIGZAGFLATINVERSE = ZIGZAGINVERSE.flatten()
ZIGZAGFLAT = np.argsort(ZIGZAGFLATINVERSE)

def zigzag_single(block):
    """
    ZigZag scan over a 8x8 2D array into a 64-element 1D array.
    Args:
        numpy.ndarray: 8x8 2D array
    Returns:
        numpy.ndarray: 64-element 1D array
    """
    return block.flatten()[ZIGZAGFLAT]

def zigzag_block(macroblock):
    """
    ZigZag scan over a 8x8x3 array into a 64x3 array.
    Args:
        numpy.ndarray: 8x8x3 array
    Returns:
        numpy.ndarray: 64x3 array
    """
    M = np.empty([64,3], dtype=macroblock.dtype)
    M[:,0] = zigzag_single(macroblock[:,:,0])
    M[:,1] = zigzag_single(macroblock[:,:,1])
    M[:,2] = zigzag_single(macroblock[:,:,2])
    return M

def zigzag(frame):
    """
    ZigZag scan over frame.
    """
    return [
        [zigzag_block(frame[x][y])
         for y in range(0, len(frame[x]))]
         for x in range(0, len(frame))
    ]

def inverse_zigzag_single(array):
    """
    Inverse ZigZag scan over 64-element 1D array into a 8x8 2D array.
    Args:
        numpy.ndarray: 64-element 1D array
    Returns:
        numpy.ndarray: 8x8 2D array
    """
    return array[ZIGZAGFLATINVERSE].reshape([8,8])

def inverse_zigzag_block(array):
    """
    Inverse ZigZag scan over a 64x3 array into a 8x8x3 array.
    Args:
        numpy.ndarray: 64x3 array
    Returns:
        numpy.ndarray: 8x8x3 array
    """
    M = np.empty([8,8,3], dtype = array.dtype)
    M[:,:,0] = inverse_zigzag_single(array[:,0])
    M[:,:,1] = inverse_zigzag_single(array[:,1])
    M[:,:,2] = inverse_zigzag_single(array[:,2])
    return M

def inverse_zigzag(frame):
    """
    Inverse ZigZag scan over frame.
    """
    return [
        [inverse_zigzag_block(frame[x][y])
         for y in range(0, len(frame[x]))]
         for x in range(0, len(frame))
    ]


if __name__ == "__main__":
    test = np.random.randint(100, size=[8,8,3])
    print(np.array_equal(test, inverse_zigzag_block(zigzag_block(test))))
