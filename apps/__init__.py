import os
import json


with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'hello/fixtures/initial_data.json'
    )
) as test_data:
    initial_data = json.load(test_data)


TEST_DATA = initial_data[1]['fields']
TEST_DATA['password'] = 'qwerty'
IMG_PATH = '~/Pictures/test.jpg'
FAKE_PATH_LIST = [
    '/fefw',
    '/12747630-426-13!@$*&_*&%!_)&@*$&__!#  *$!@$*_!%)(&#*$&&$)!(#$)(',
    '/',
    '/el/',
    '/www',
    '/1242',
    '/?d=3',
    '/?_=23423523',
    '/avaba-kedabra/',
    '/****/'
]
