import numpy as np

def compute_reference(blocks, reference):
    """For every block returns a pair, (offset, residual),
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
            offset, residual = find_match(block, reference, offset_x, offset_y)
            offsets[-1].append(offset)
            residuals[-1].append(residual)
            offset_y += block.shape[1]
        offset_x += blocks_row[0].shape[0]
    return offsets, residuals

def apply_reference(offsets, residuals, reference):
    """Inverse of compute_reference"""
    result = []
    offset_x = 0
    for offsets_row, residuals_row in zip(offsets, residuals):
        result.append([])
        offset_y = 0
        for (dx,dy), residual in zip(offsets_row, residuals_row):
            bl_x, bl_y, _ = residual.shape
            new_x, new_y = offset_x + dx, offset_y + dy
            reference_block = reference[new_x:new_x+bl_x, new_y:new_y +bl_y, :]
            recovered_block = (reference_block + residual).astype(np.uint8)
            result[-1].append(recovered_block)
            offset_y += residual.shape[1]
        offset_x += residuals_row[0].shape[0]
    return result

def cost_f(block1, block2):
    """Computes the cost of the block pairing"""
    return abs(block1 - block2).sum()

def find_match(block, reference, offset_x, offset_y, max_delta=2):
    """Given a block, find the best match for that block in reference image
    returns offset and residual error"""
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
    return best_offset, block.astype(np.int16) - best_ref
