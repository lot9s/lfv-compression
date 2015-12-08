from our_mpeg import decode, encode, load
import sys

print('loading...', flush=True)
image_data = load(sys.argv[1])
print('finished loading')
sys.stdout.flush()

test_image_1 = image_data[0][0][0]
test_image_2 = image_data[0][0][1]

print('encoding...')
encoded = encode(test_image_1, test_image_2, 4)
print('finished encoding')

print('decoding...')
decoded = decode(encoded, test_image_2, 4)
print('finished decoding')

print(test_image_1 == decoded)
