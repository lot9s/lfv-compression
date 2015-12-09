import numpy as np
from PIL import Image
from zipfile import ZipFile
import sys
import re
try:
    from StringIO import StringIO as IOWrapper
except ImportError:
    from io import BytesIO as IOWrapper


def load(zipfile):
    """Loads the light field video file, and returns the results as a tensor with dimensions
        (timestep, camera_x, camera_y, image_x, image_y, color)"""
    LFV = {}
    archive = ZipFile(zipfile, 'r')
    n_time, n_camera_x, n_camera_y, image_x, image_y = 0, 0, 0, 0, 0
    for time, camera_x, camera_y, filename in iterate_archive(archive):
        n_time = max(n_time, time + 1)
        n_camera_x = max(n_camera_x, camera_x + 1)
        n_camera_y = max(n_camera_y, camera_y + 1)
        if image_x == 0:
            data = _open_ycbr_from_archive(filename, archive)
            image_x, image_y, _ = data.shape

    result = np.empty((n_time, n_camera_x, n_camera_y, image_x, image_y, 3), dtype=np.uint8)
    
    for time, camera_x, camera_y, filename in iterate_archive(archive):
        data = _open_ycbr_from_archive(filename, archive)
        result[time, camera_x, camera_y, :, :, :] = data

    return result

def load_separate(zipfile):
    """Loads the light field video file, and returns the results as three tensors Y, Cb, Cr each with dimensions
        (timestep, camera_x, camera_y, image_x, image_y)"""
    return [np.squeeze(x) for x in np.split(load(zipfile),3,5)]

def iterate_archive(archive):
    for entry in archive.infolist():
        filename = entry.filename
        if filename[-4:] == '.png':  #only open png
            path = filename.split('/')
            cameras = re.match(r'^camera_(\d+)_(\d+)$', path[0])
            camera_x = int(cameras.group(1))
            camera_y = int(cameras.group(2))
            time = int(re.match(r'^Image(\d+).png$', path[1]).group(1)) - 1
            yield time, camera_x, camera_y, filename

def _open_ycbr_from_archive(filename, archive):
    image_data =  archive.read(filename)
    fh = IOWrapper(image_data)
    image = Image.open(fh)
    ycbr = image.convert('YCbCr')
    return np.ndarray(shape=(image.size[1], image.size[0], 3), dtype=np.uint8, buffer=ycbr.tobytes())
