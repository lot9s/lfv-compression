import numpy as np
import sys

from os import listdir
from os.path import join
from PIL import Image


def nparray_size_bytes(arr):
    number_of_elements = 1
    for dim in arr.shape:
        number_of_elements *= dim
    return number_of_elements * arr.dtype.itemsize

def compute_uncompressed_size(lf_video):
    total_size = 0
    cameras = listdir(lf_video)
    for camera in cameras:
        camera_path = join(lf_video, camera)
        for image_name in sorted(listdir(camera_path)):
            image_path = join(camera_path, image_name)
            image = Image.open(image_path)
            total_size += nparray_size_bytes(np.array(image))
    return total_size

if __name__ == '__main__':
    print('FL video', sys.argv[1], 'has size', compute_uncompressed_size(sys.argv[1]), 'bytes.')
