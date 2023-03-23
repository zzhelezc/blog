#!/usr/bin/env python

try:
    from StringIO import StringIO as sbIO
except ImportError:
    from io import BytesIO as sbIO
import struct
import os
import sys
import json
import re
from collections import OrderedDict

PATH = os.path.dirname(__file__) + '/../'
RELATIVE_PATH = 'gallery/photos'
PHOTO_PATH = PATH + RELATIVE_PATH

titles = {
    "./photos/People/0.jpg": "Bristol, UK, 2023",
    "./photos/People/1.jpg": "Bristol, UK, 2023",
    "./photos/People/2.jpg": "Bristol, UK, 2023"
}

# photos = OrderedDict({
#     "People": [f'{i}.jpg' for i in range(10)],
#     "People Alone": [f'{i}.jpg' for i in range(10, 23)],
#     "Places and Things": [f'{i}.jpg' for i in range(23, 44)]
# })

photos = OrderedDict({
    "People": ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg',
               '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg'],

    
    "People Alone": ['10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg',
                     '15.jpg', '16.jpg', '17.jpg', '18.jpg', '19.jpg',
                     '20.jpg', '21.jpg', '22.jpg'],
    
    "Places and Things": ['23.jpg', '24.jpg', '25.jpg', '26.jpg', '27.jpg',
                          '28.jpg', '29.jpg', '30.jpg', '31.jpg', '32.jpg',
                          '33.jpg', '34.jpg', '35.jpg', '36.jpg', '37.jpg',
                          '38.jpg', '39.jpg', '40.jpg', '41.jpg', '42.jpg', '43.jpg']
})


print(photos["People"])
print(photos["People Alone"])
print(photos["Places and Things"])

def is_original(path):
    return '.min.' not in path and '.placeholder.' not in path and is_image_path(path)


def is_not_min_path(path):
    return not is_min_path(path) and is_image_path(path)


def is_min_path(path):
    return '.min.' in path and is_image_path(path)


def get_directories():
    items = os.listdir(PHOTO_PATH)
    return list(filter(lambda x: os.path.isdir(PHOTO_PATH + '/' + x), items))


def is_image_path(path):
    return re.search(r'\.(jpe?g|png)$', path)


def get_placeholder_path(path):
    return get_path(path, 'placeholder')


def get_min_path(path):
    return get_path(path, 'min')


def get_path(path, ext):
    return re.sub(r'\.(png|jpe?g)$', '.' + ext + '.\g<1>', path)


def get_images(path):
    items = os.listdir(PHOTO_PATH + '/' + path)
    #filtered_items = list(filter(is_original, items))
    filtered_items = photos[path]
    result = []

    
    
    filtered_items.reverse()
    print(filtered_items)
    for img in filtered_items:
        width, height = 0, 0
        has_compressed = False
        p = './' + 'photos' + '/' + path + '/' + img
        with open(PHOTO_PATH + '/' + path + '/' + img, 'rb') as f:
            _, width, height = getImageInfo(f.read())
        if os.path.isfile(get_min_path(p)):
            has_compressed = True
        
        final_path = './' + 'photos' + '/' + path + '/' + img
        result.append({
            'width': width,
            'height': height,
            'path': final_path,
            'compressed_path': get_min_path(p),
            'compressed': has_compressed,
            'placeholder_path': get_placeholder_path(p),
            'title': titles.get(final_path, "Untitled")
        })
    return result


def write_config(config):
    with open('gallery/config.json', 'w') as f:
        f.write(json.dumps(config, indent=2, separators=(',', ': ')))


def run():
    print('Starting to collect all albums within the /photos directory...')
    config = OrderedDict()
    #dirs = get_directories()
    dirs = list(photos.keys())
    print(dirs)
    print('Found {length} directories'.format(length=len(dirs)))
    for i, path in enumerate(dirs):
        print(str(i+1) + ': Processing photos for the album "{album}"'.format(
            album=path))
        images = get_images(path)
        config[path] = images 

        print('   Done processing {l} photos for "{album}"\n'.format(
            l=len(config[path]),
            album=path))

    print('Done processing all {length} albums'.format(length=len(dirs)))
    print('Writing files to {path} now...'.format(path=PATH + 'config.json'))
    write_config(config)
    print('''Done writing! You may now safely close this window :)

Thank you for using gallery! Share your gallery on Github!
https://github.com/andyzg/gallery/issues/1''')
    return 0


############################################################
# Thanks StackOverflow: http://stackoverflow.com/a/3175473 #
############################################################
def getImageInfo(data):
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    if ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n') and
       (data[12:16] == b'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith(b'\xff\xd8'):
        content_type = 'image/jpeg'

        try:
            jpeg = sbIO(data)  # Python 3
        except:
            jpeg = sbIO(str(data))  # Python 2

        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF):
                    b = jpeg.read(1)
                while (ord(b) == 0xFF):
                    b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height

if __name__ == '__main__':
    sys.exit(run())
