import numpy as np

def compute_dual_reference(blocks, reference1, reference2):
    """For every block returns a pair, (offset, residual1, residual2),
    where offset is the offet wrt initial position of block in the image,
    such that the residual is calculated w.r.t reference image position
    (block_position + offset)"""
    offsets   = []
    residuals = []
    offset_x = 0
    for blocks_row in blocks:
        offsets.append([])
        residuals.append([])
        offset_y = 0
        for block in blocks_row:
            offset1, ref_block1 = find_match(block, reference1, offset_x, offset_y)
            offset2, ref_block2 = find_match(block, reference2, offset_x, offset_y)
            residual = block.astype(np.int16) - (ref_block1.astype(np.int16) + ref_block2) // 2
            assert residual.dtype == np.int16
            offsets[-1].append((offset1, offset2))
            residuals[-1].append(residual)
            offset_y += block.shape[1]
        offset_x += blocks_row[0].shape[0]
    return offsets, residuals

def find_delta(from_image, to_image, delta=30, pattern_radius = 20):
   best, best_d = float('inf'), None
   for dx in range(-delta,delta+1):
       for dy in range(-delta,delta+1):
           patternA = to_image[cx-pattern_radius:cx+pattern_radius,cy-pattern_radius:cy+pattern_radius]
           patternB = from_image[cx+dx-pattern_radius:cx+dx+pattern_radius,cy+dy-pattern_radius:cy+dy+pattern_radius]
           score = abs(patternA.astype(np.float32) - patternB.astype(np.float32)).sum()
           if score < best:
               best = score
               best_d = (dx,dy)
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
            new_x1, new_y1 = offset_x + dx1, offset_y + dy1
            new_x2, new_y2 = offset_x + dx2, offset_y + dy2
            reference_block1 = reference1[new_x1:new_x1+bl_x, new_y1:new_y1 +bl_y, :]
            reference_block2 = reference2[new_x2:new_x2+bl_x, new_y2:new_y2 +bl_y, :]
            recovered_block = ((reference_block1.astype(np.int16) + reference_block2) // 2 + residual).astype(np.uint8)
            result[-1].append(recovered_block)
            offset_y += residual.shape[1]
        offset_x += residuals_row[0].shape[0]
    return result

def cost_f(block1, block2):
    """Computes the cost of the block pairing"""
    return abs(block1 - block2).sum()

def find_match(block, reference, offset_x, offset_y, max_delta=3):
    """Given a block, find the best match for that block in reference image
    returns offset and reference block"""
    bl_x, bl_y, _ = block.shape
    best_cost = float('inf')
    best_offset = (None, None)
    best_ref = None
    for dx in range(-max_delta, max_delta + 1):
        for dy in range(-max_delta, max_delta + 1):
            new_x, new_y = offset_x + dx, offset_y + dy
            reference_block = reference[new_x:new_x+bl_x, new_y:new_y +bl_y, :]
            if reference_block.shape != block.shape:
                continue
            new_cost = cost_f(block, reference_block)
            if new_cost < best_cost:
                best_cost = new_cost
                best_offset = (dx,dy)
                best_ref = reference_block
    return best_offset, best_ref
