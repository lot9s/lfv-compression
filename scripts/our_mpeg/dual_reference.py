import numpy as np

from .reference import find_match

FUNNY_OFFSET = 63

def compute_dual_reference(blocks, reference1, reference2, delta1, delta2, single_grid=2, double_grid=2):
    """For every block returns a pair, (offset, residual1, residual2),
    where offset is the offet wrt initial position of block in the image,
    such that the residual is calculated w.r.t reference image position
    (block_position + offset)"""

    reference1 = reference1.astype(np.float32)
    reference2 = reference2.astype(np.float32)

    offsets   = []
    residuals = []
    offset_x = 0
    for blocks_row in blocks:
        offsets.append([])
        residuals.append([])
        offset_y = 0
        for block in blocks_row:
            best_norm      = np.linalg.norm(block)
            best_offsets   = ((FUNNY_OFFSET, FUNNY_OFFSET), (FUNNY_OFFSET, FUNNY_OFFSET))
            best_residual  = block

            # only use reference image 1
            (x1,y1), residual = find_match(block, reference1, offset_x + delta1[0], offset_y + delta1[1], max_delta=single_grid)
            if residual is not None and np.linalg.norm(residual) < best_norm:
                best_norm = np.linalg.norm(residual)
                best_residual = residual
                best_offsets = ((x1 + delta1[0], y1 + delta1[1]), (FUNNY_OFFSET, FUNNY_OFFSET))

            # only use reference image 2
            (x2,y2), residual = find_match(block, reference2, offset_x + delta2[0], offset_y + delta2[1], max_delta=single_grid)
            if residual is not None and np.linalg.norm(residual) < best_norm:
                best_norm = np.linalg.norm(residual)
                best_residual = residual
                best_offsets = ((FUNNY_OFFSET, FUNNY_OFFSET),  (x2 + delta2[0], y2 + delta2[1]))

            for (x1, y1), ref_block1 in iterate_blocks(block, reference1, offset_x + delta1[0], offset_y + delta1[1], max_delta=double_grid):
                for (x2, y2), ref_block2 in iterate_blocks(block, reference2, offset_x + delta2[0], offset_y + delta2[1], max_delta=double_grid):
                    residual = block - (ref_block1 + ref_block2) / 2.0
                    cost = np.linalg.norm(residual)
                    if cost < best_norm:
                        best_norm = cost
                        best_offsets = ((x1 + delta1[0], y1 + delta1[1]), (x2 + delta2[0], y2 + delta2[1]))
                        best_residual = residual

            offsets[-1].append(best_offsets)
            residuals[-1].append(best_residual)
            offset_y += block.shape[1]
        offset_x += blocks_row[0].shape[0]
    return offsets, residuals

def find_delta(from_image, to_image, delta=30, pattern_radius = 20):
    assert from_image.shape == to_image.shape
    cx, cy = from_image.shape[0] // 2, from_image.shape[1] // 2
    best, best_d = float('inf'), None
    for dx in range(-delta,delta+1):
        for dy in range(-delta,delta+1):
            patternA = to_image[cx-pattern_radius:cx+pattern_radius,cy-pattern_radius:cy+pattern_radius]
            patternB = from_image[cx+dx-pattern_radius:cx+dx+pattern_radius,cy+dy-pattern_radius:cy+dy+pattern_radius]
            score = abs(patternA.astype(np.float32) - patternB.astype(np.float32)).sum()
            if score < best:
                best = score
                best_d = (dx,dy)
    assert best_d is not None
    return best_d

def apply_dual_reference(offsets, residuals, reference1, reference2):
    """Inverse of compute_reference"""
    result = []
    offset_x = 0
    for offsets_row, residuals_row in zip(offsets, residuals):
        result.append([])
        offset_y = 0
        for ((dx1,dy1),(dx2,dy2)), residual in zip(offsets_row, residuals_row):
            bl_x, bl_y, _ = residual.shape
            if not (dx1 == FUNNY_OFFSET and dy1 == FUNNY_OFFSET):
                new_x1, new_y1 = offset_x + dx1, offset_y + dy1
                reference_block1 = reference1[new_x1:new_x1+bl_x, new_y1:new_y1 +bl_y, :].astype(np.float32)
                reference_block1 = reference_block1 if reference_block1.shape == residual.shape else np.zeros_like(residual)
            else:
                reference_block1 = np.zeros_like(residual)

            if not (dx2 == FUNNY_OFFSET and dy2 == FUNNY_OFFSET):
                new_x2, new_y2 = offset_x + dx2, offset_y + dy2
                reference_block2 = reference2[new_x2:new_x2+bl_x, new_y2:new_y2 +bl_y, :].astype(np.float32)
                reference_block2 = reference_block2 if reference_block2.shape == residual.shape else np.zeros_like(residual)
            else:
                reference_block2 = np.zeros_like(residual)

            total_reference = reference_block1 + reference_block2

            if ((not (dx1 == FUNNY_OFFSET and dy1 == FUNNY_OFFSET)) and
                    (not (dx2 == FUNNY_OFFSET and dy2 == FUNNY_OFFSET))):
                total_reference /= 2.0

            recovered_block = total_reference + residual

            result[-1].append(recovered_block)
            offset_y += residual.shape[1]
        offset_x += residuals_row[0].shape[0]
    return result

def iterate_blocks(block, reference, offset_x, offset_y, max_delta=2):
    """FIXME"""
    bl_x, bl_y, _ = block.shape

    for dx in range(-max_delta, max_delta + 1):
        for dy in range(-max_delta, max_delta + 1):
            new_x, new_y = offset_x + dx, offset_y + dy
            reference_block = reference[new_x:new_x+bl_x, new_y:new_y +bl_y, :]
            if reference_block.shape != block.shape:
                continue
            yield (dx, dy), reference_block
