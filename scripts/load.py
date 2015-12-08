import numpy
import Image
from zipfile import ZipFile
import sys
import re
from StringIO import StringIO

# #Structure:   LFV[File]['Y', 'Cb', or 'Cr'][x][y]
# def load_old(zipfile):
# 	LFV = {}
# 	archive = ZipFile(zipfile, 'r')
# 	for entry in archive.infolist():
# 		filename = entry.filename
# 		print filename
# 		if filename[-4:] == '.png':  #only open png
# 			ycbr_array = _open_file_ycbr(filename, archive)
# 			y = [[x[0] for x in ycbr_row] for ycbr_row in ycbr_array]
# 			Cb = [[x[1] for x in ycbr_row] for ycbr_row in ycbr_array]
# 			Cr = [[x[2] for x in ycbr_row] for ycbr_row in ycbr_array]

# 			LFV[filename] = {}
# 			LFV[filename]['Y'] = y
# 			LFV[filename]['Cb'] = Cb
# 			LFV[filename]['Cr'] = Cr

# 	return LFV

#Structure: LFV[camera_x][camera_y][time][x][y][Y=0, Cb=1, Cr=2]
def load(zipfile):
	LFV = {}
	archive = ZipFile(zipfile, 'r')
	for entry in archive.infolist():
		filename = entry.filename
		print 'opening: {}'.format(filename)
		if filename[-4:] == '.png':  #only open png
			path = filename.split('/')
			cameras = re.match(r'^camera_(\d+)_(\d+)$', path[0])
			camera_x = int(cameras.group(1))
			camera_y = int(cameras.group(2))
			time = int(re.match(r'^Image(\d+).png$', path[1]).group(1))
			data = _open_ycbr_from_archive(filename, archive)
			current = LFV
			for p in [camera_x, camera_y, time]:
				if p not in current.keys():
					current[p] = {}
				current = current[p]
			LFV[camera_x][camera_y][time] = data
	return _make_list(LFV)

#note: all keys must be castable to integer
def _make_list(dictionary):
	if isinstance(dictionary, dict):
		return [dictionary[i] for i in xrange(len(dictionary))]
	return dictionary

def _open_ycbr_from_archive(filename, archive):
	image_data =  archive.read(filename)
	fh = StringIO(image_data)
	image = Image.open(fh)
	ycbr = image.convert('YCbCr')
	return numpy.ndarray((image.size[1], image.size[0], 3), 'u1', ycbr.tostring())


# USAGE: load_lf_video <video_file_name>.zip
load(sys.argv[1])