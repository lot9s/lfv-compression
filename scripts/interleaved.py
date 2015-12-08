#!/usr/bin/python
import os
import shutil
import subprocess
import sys
import time

from itertools import count
from PIL import Image
from tempfile import TemporaryDirectory

IMG_EXT       = '.png'
IMG_PREFIX    = 'Image'
CAMERA_PREFIX = 'camera_'

# -- Functions ---
# this method produces the properly formatted path to the desired image
def GetImgPath(img_dir, camera, t):
    img_file = '%s%04d%s' % (IMG_PREFIX, t, IMG_EXT)
    return os.path.join(img_dir, camera, img_file)

# this method produces the properly formatted path to the desired output image
def GetOutImgPath(out_dir, t):
    return os.path.join(out_dir, 'out-%04d%s' % (t,IMG_EXT))

def extract_coordinates(camera_folder):
    assert camera_folder.startswith(CAMERA_PREFIX)
    x, y = camera_folder[len(CAMERA_PREFIX):].split('_')
    return int(x), int(y)

def GetCameraPath(x,y):
    return '%s%d_%d' % (CAMERA_PREFIX, x, y)

# --- Script ---
# ensure proper usage
if len(sys.argv) != 2:
    print('USAGE:\t./stitcher.py img-dir')
    sys.exit()
lf_video_dir = sys.argv[1]

# ensure that the output directory is there when we need it
with TemporaryDirectory() as output_dir:
    # get cmd line args
    camera_dirs = os.listdir(lf_video_dir)
    camera_coordinates = [ extract_coordinates(d) for d in camera_dirs]
    cam_rows = max([x for x,y in camera_coordinates])
    cam_cols = max([y for x,y in camera_coordinates])

    # get info about images
    init_img = Image.open(GetImgPath(lf_video_dir, camera_dirs[0], 1))
    img_width = init_img.size[0]
    img_height = init_img.size[1]

    camera_order = []
    temp_columns = list(range(cam_cols))
    for row in range(cam_rows):
        # temp_columns = list(reversed(temp_columns))
        for col in temp_columns:
            camera_order.append((row,col))

    # create output image
    fake_timestep = 1
    for timestep in count(1):
        if not os.path.exists(GetImgPath(lf_video_dir, camera_dirs[0], timestep)):
            break
        camera_order = list(reversed(camera_order))
        for row, col in camera_order:
            image_path = GetImgPath(lf_video_dir, GetCameraPath(row,col), timestep)
            output_image_path = GetOutImgPath(output_dir, fake_timestep)
            fake_timestep += 1
            print ("Moving %s to %s." % (image_path, output_image_path))
            img_out = Image.open(image_path)
            img_out.save(output_image_path)
    print("Merging frames...")

    #  "-force_key_frames", "expr:gte(n, n_forced*%d)" % (len(camera_order),),
    p = subprocess.Popen(["ffmpeg", "-r", "24", "-pattern_type" , "glob", "-i", "*.png", "-c:v", "libx264", "out.mp4"], cwd=output_dir)
    p.wait()
    shutil.move(os.path.join(output_dir, 'out.mp4'), os.getcwd())
