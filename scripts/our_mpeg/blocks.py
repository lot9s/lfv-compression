import numpy as np

def break_blocks(image, block_size=8):
    """Breaks image into blocks of size block_size by block_size or less on the edges
    returns a 2D array of blocks that corresponds to the grid which the blocks
    from on top of the image."""
    return [
        [image[start_x:start_x+block_size, start_y:start_y+block_size, :].astype(np.float32)
         for start_y in range(0, len(image[0]), block_size)]
         for start_x in range(0, len(image), block_size)
    ]

def merge_blocks(blocks):
    """Inverse of break_blocks"""
    bl_x, bl_y = len(blocks), len(blocks[0])
    size_x = sum([blocks[i][0].shape[0] for i in range(bl_x)])
    size_y = sum([blocks[0][i].shape[1] for i in range(bl_y)])
    result = np.empty((size_x, size_y, 3), dtype=np.uint8)
    offset_x = 0
    for blocks_row in blocks:
        offset_y = 0
        for block in blocks_row:
            cur_x, cur_y, _ = block.shape
            result[offset_x:offset_x+cur_x, offset_y:offset_y+cur_y, :] = np.round(np.clip(block, 0, 255.0, )).astype(np.uint8)
            offset_y += cur_y
        offset_x += blocks_row[0].shape[0]
    return result
