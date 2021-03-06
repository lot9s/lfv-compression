from our_mpeg import compute_reference, apply_reference
from our_mpeg import transform, inverse_transform
from our_mpeg import quantize, dequantize
from our_mpeg import break_blocks, merge_blocks
from our_mpeg import compute_dual_reference, apply_dual_reference, find_delta

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

def compress_image_with_reference(im1, reference_image, block_size=8):
    im1_blocks = break_blocks(im1, block_size=8)
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

def compress_image_with_dual_reference(im1, reference_image1, reference_image2, block_size=8, single_grid=2, double_grid=2):
    im1_blocks = break_blocks(im1, block_size=8)
    d1 = find_delta(reference_image1, im1)
    d2 = find_delta(reference_image2, im1)
    im1_offsets, im1_residuals = compute_dual_reference(im1_blocks, reference_image1, reference_image2, d1, d2, single_grid=single_grid, double_grid=double_grid)
    im1_residuals_dct = transform(im1_residuals)
    im1_residuals_q = quantize(im1_residuals_dct)
    return im1_offsets, im1_residuals_q

def decompress_image_with_dual_reference(im1_offsets, im1_residuals_q, reference_image1, reference_image2):
    im1_residuals_dq = dequantize(im1_residuals_q)
    im1_residuals_idct = inverse_transform(im1_residuals_dq)
    im1_blocks_recovered = apply_dual_reference(im1_offsets, im1_residuals_idct, reference_image1, reference_image2)
    im1_recovered = merge_blocks(im1_blocks_recovered)
    return im1_recovered
