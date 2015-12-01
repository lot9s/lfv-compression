import numpy
import Image
from zipfile import ZipFile
import sys
from StringIO import StringIO

# USAGE: load_lf_video <video_file_name>.zip

archive = ZipFile(sys.argv[1], 'r')
for entry in archive.infolist():
	filename = entry.filename
	if filename[-4:] == '.png':  #only open png
		print filename
		image_data =  archive.read(filename)
		fh = StringIO(image_data)
		image = Image.open(fh)
		ycbr = image.convert('YCbCr')
		ycbr_array = numpy.ndarray((image.size[1], image.size[0], 3), 'u1', ycbr.tostring())
		print ycbr_array
		# TODO: DO THINGS WITH THE ycbr array
		exit(0)  #Exit after the first right now so we dont print out a ton of stuff