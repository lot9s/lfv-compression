import numpy as np
import sys

from our_mpeg import load, load_separate
from our_mpeg import break_blocks, merge_blocks
from our_mpeg import compute_reference, apply_reference
from our_mpeg import transform, inverse_transform
from our_mpeg import quantize, dequantize

print('loading...', flush=True)
image_data = load(sys.argv[1])
print('finished loading')
sys.stdout.flush()

im1 = image_data[0,0,0]
im2 = image_data[1,0,0]

print('encoding...')

im1_blocks = break_blocks(im1)
im1_offsets, im1_residuals = compute_reference(im1_blocks, im2)
im1_residuals_dct = transform(im1_residuals)
im1_residuals_q = quantize(im1_residuals_dct)
print('finished encoding')

print('decoding...')
im1_residuals_dq = dequantize(im1_residuals_q)
im1_residuals_idct = inverse_transform(im1_residuals_dq)
im1_blocks_recovered = apply_reference(im1_offsets, im1_residuals_idct, im2)
im1_recovered = merge_blocks(im1_blocks_recovered)

print('finished decoding')

print(np.linalg.norm(im1_recovered - im1))
