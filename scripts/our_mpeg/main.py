from our_mpeg import compute_reference, apply_reference
from our_mpeg import transform, inverse_transform
from our_mpeg import quantize, dequantize
from our_mpeg import break_blocks, merge_blocks

def compress_image(im1):
    im1_blocks = break_blocks(im1)
    im1_blocks_dct = transform(im1_blocks)
    im1_blocks_q = quantize(im1_blocks_dct)
    return im1_blocks_q

def decompress_image(im1_blocks_q):
    im1_blocks_dq = dequantize(im1_blocks_q)
    im1_blocks_idct = inverse_transform(im1_blocks_dq)
    im1_recovered = merge_blocks(im1_blocks_idct)
    return im1_recovered

def compress_image_with_reference(im1, reference_image):
    im1_blocks = break_blocks(im1)
    im1_offsets, im1_residuals = compute_reference(im1_blocks, reference_image)
    im1_residuals_dct = transform(im1_residuals)
    im1_residuals_q = quantize(im1_residuals_dct)
    return im1_offsets, im1_residuals_q

def decompress_image_with_reference(im1_offsets, im1_residuals_q, reference_image):
    im1_residuals_dq = dequantize(im1_residuals_q)
    im1_residuals_idct = inverse_transform(im1_residuals_dq)
    im1_blocks_recovered = apply_reference(im1_offsets, im1_residuals_idct, reference_image)
    im1_recovered = merge_blocks(im1_blocks_recovered)
    return im1_recovered
