import scipy.fftpack
import numpy

global block_size

#image and reference are 2d arrays of [y, cb, cr] lists
#image size must be multiple of block size (for now)
def encode(image, reference, block_dim):
	global block_size
	block_size = block_dim
	iterations_x = len(image)//block_size
	iterations_y = len(image[0])//block_size
	return [[_find_match(image, x, y, reference) for y in range(iterations_y)] for x in range(iterations_x)]

#finds the best match given the _image_iterator pattern of selecting reference images
def _find_match(image, x, y, reference):
	encode_block = _get_block(image, x, y)
	min_coordinates = None
	min_block = None
	min_value = float('inf')
	for (ref_block, ref_x, ref_y) in _image_iterator(reference, x, y):
		dist = _block_dist(encode_block, ref_block)
		if dist < min_value:
			min_value = dist
			min_coordinates = (ref_x, ref_y)
			min_block = ref_block
	motion_vector = (min_coordinates[0] - x, min_coordinates[1] - y)
	residual = scipy.fftpack.dct(_residual_block(encode_block, min_block))
	return (motion_vector, residual)

def _get_block(image, x, y):
	return image[x:x+block_size, [i+y for i in range(block_size)]]

def _residual_block(encode_block, ref_block):
	residual = numpy.subtract(encode_block, ref_block)

def _block_dist(a, b):
	total = 0
	for i in range(len(a)):
		for j in range(len(a[i])):
			for k in range(len(a[i][j])):
				total += _absolute_differences(a[i][j][k], b[i][j][k])
	return total

#comparrision algorithm
def _sum_of_squares_comp(a, b):
	return (int(a) - int(b))**2

#comparrision algorithm
def _absolute_differences(a, b):
	return abs(int(a) - int(b))


#this class returns the block to search in an image.
#TODO: currently uses a full search of the reference image.  Implement a faster search if neccessary
def _image_iterator(image, start_x, start_y):
	for x in range(len(image) - block_size + 1):
		for y in range(len(image[x]) - block_size + 1):
			yield (_get_block(image, x, y), x, y)