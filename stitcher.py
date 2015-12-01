#!/usr/bin/python


from PIL import Image

import os
import sys


IMG_EXT = '.png'
IMG_PREFIX = '/Image'
OUT_DIR = 'out/'


# -- Functions ---
# this method produces the properly formatted path to the desired image
def GetImgPath(img_dir, cam, t): 
    return (img_dir + str(cam) + IMG_PREFIX + '%04d' + IMG_EXT) % t
    
# this method produces the properly formatted path to the desired output image
def GetOutImgPath(t):
    return (OUT_DIR + 'out-' + '%04d' + IMG_EXT) % t 


# --- Script ---
# ensure proper usage
if len(sys.argv) < 4:
    print 'USAGE:\t./stitcher.py img-dir grid-layout t-max'
    print 'ex.\t./stitcher.py data/ 2x2 72'
    sys.exit()
    
# ensure that the output directory is there when we need it
if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)
    
# get cmd line args
img_dir = sys.argv[1]
grid_layout = sys.argv[2].split('x')
t_max = int(sys.argv[3])

# get info about images
t0 = 1
cam = 0
init_img = Image.open(GetImgPath(img_dir, cam, t0))
img_width = init_img.size[0]
img_height = init_img.size[1]

# create output image
cam_rows = int(grid_layout[0])
cam_cols = int(grid_layout[1])
for t in range(t0, t_max):
    img_out = Image.new('RGB', (img_width * cam_cols, img_height * cam_rows))
    for row in range(cam_rows):
        for col in range(cam_cols):
            img_temp = Image.open(GetImgPath(img_dir, (row * cam_rows) + col, t))
            img_out.paste(img_temp, (img_width * col, img_height * row))
    img_out.save(GetOutImgPath(t))
