import numpy
import Image
from zipfile import ZipFile
import sys
from StringIO import StringIO

#Structure:   LFV[File]['Y', 'Cb', or 'Cr'][x][y]

def load(zipfile):
	LFV = {}
	archive = ZipFile(zipfile, 'r')
	for entry in archive.infolist():
		filename = entry.filename
		if filename[-4:] == '.png':  #only open png
			image_data =  archive.read(filename)
			fh = StringIO(image_data)
			image = Image.open(fh)
			ycbr = image.convert('YCbCr')
			ycbr_array = numpy.ndarray((image.size[1], image.size[0], 3), 'u1', ycbr.tostring())
			y = [[x[0] for x in ycbr_row] for ycbr_row in ycbr_array]
			Cb = [[x[1] for x in ycbr_row] for ycbr_row in ycbr_array]
			Cr = [[x[2] for x in ycbr_row] for ycbr_row in ycbr_array]

			LFV[filename] = {}
			LFV[filename]['Y'] = y
			LFV[filename]['Cb'] = Cb
			LFV[filename]['Cr'] = Cr

	return LFV



# USAGE: load_lf_video <video_file_name>.zip
load(sys.argv[1])