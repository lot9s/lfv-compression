import numpy as np
import sys

from our_mpeg import load
from our_mpeg import break_blocks, merge_blocks
from our_mpeg import compute_reference, apply_reference


print('loading...', flush=True)
image_data = load(sys.argv[1])
print('finished loading')
sys.stdout.flush()

test_image_1 = image_data[0,0,0]
test_image_2 = image_data[1,0,0]

print('encoding...')
im1_blocks = break_blocks(test_image_1)
im1_ref    = compute_reference(im1_blocks, test_image_2)
print('finished encoding')

print('decoding...')
im1_blocks_recovered    = apply_reference(im1_ref, test_image_2)

im1_recovered = merge_blocks(im1_blocks_recovered)
print('finished decoding')

print(np.linalg.norm(im1_recovered - test_image_1))
