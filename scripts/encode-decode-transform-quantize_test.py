import numpy as np
import sys

from our_mpeg import load, load_separate
from our_mpeg import break_blocks, merge_blocks
from our_mpeg import compute_reference, apply_reference
from our_mpeg import transform, inverse_transform
from our_mpeg import quantize_inter, dequantize_inter, quantize_intra, dequantize_intra

print('loading...', flush=True)
image_data = load(sys.argv[1])
print('finished loading')
sys.stdout.flush()

test_image_1 = image_data[0,0,0]
test_image_2 = image_data[1,0,0]


print('encoding...')
im1_blocks = break_blocks(test_image_1)
im1_ref = compute_reference(im1_blocks, test_image_2)

# transform the residuals...
im1_res = [[im1_ref[x][y][1] for y in range(0, len(im1_ref[x]))] for x in range(0, len(im1_ref))]

im1_res_trans = transform(im1_res)

# inter-quantize residuals
im1_res_q = quantize_inter(im1_res_trans)
print('finished encoding')

print('decoding...')
# inter-dequantize residuals
im1_res_dq = dequantize_inter(im1_res_q)

# inverse transform the residuals
im1_res_inv_trans = inverse_transform(im1_res_dq)

# check if the inverse transform gave back the original
im1_ref_recovered = [[(im1_ref[x][y][0],im1_res_inv_trans[x][y]) for y in range(0, len(im1_res_inv_trans[x]))] for x in range(0, len(im1_res_inv_trans))]

im1_blocks_recovered = apply_reference(im1_ref_recovered, test_image_2)

im1_recovered = merge_blocks(im1_blocks_recovered)
print('finished decoding')

print(np.linalg.norm(im1_recovered - test_image_1))
