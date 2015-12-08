import numpy
import scipy

global block_size

def decode(blocks, reference, block_dim):
	global block_size
	block_size = block_dim

	recovered_image = [[[]]]
	for block_x in xrange(len(blocks)):
		column = [[]]
		for block_y in xrange(len(blocks[block_x])):
			motion_vect, residual = blocks[block_x][block_y]
			ref_x = block_x*block_size + motion_vect[0]
			ref_y = block_y*block_size + motion_vect[1]
			recovered_block = _recover_block(ref_x, ref_y, reference, residual)
			column = numpy.concatenate((column, [recovered_block]), axis=0)
		recovered_image = numpy.concatenate((recovered_image, [column]), axis=0)

	return recovered_image

def _recover_block(x, y, reference, residual):
	reference_block = _get_block(reference, x, y)
	residual_decoded = scipy.fftpack.idct(residual)
	return numpy.add(reference_block, residual_decoded)


def _get_block(image, x, y):
	return image[x:x+block_size][y:y+block_size]