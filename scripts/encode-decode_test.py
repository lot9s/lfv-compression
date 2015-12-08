import load
import mpeg_encode
import mpeg_decode

print 'loading...'
image_data = load.load('../bottle.zip')
print 'finished loading'

test_image_1 = image_data[0][0][0]
test_image_2 = image_data[0][0][1]

print 'encoding...'
encoded = mpeg_encode.encode(test_image_1, test_image_2, 4)
print 'finished encoding'

print 'decoding...'
decoded = mpeg_decode.decode(encoded, test_image_2, 4)
print 'finished decoding'

print test_image_1 == decoded