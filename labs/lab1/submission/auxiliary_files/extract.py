#!/usr/bin/env python
import sys, struct, numpy, PIL as pillow
from PIL import Image

def decompose(data):
    v = []
    fSize = len(data)
    bytes = [ ord(b) for b in struct.pack('i', fSize) ]
    bytes += [ ord(b) for b in data ]
    for b in bytes:
        for i in range(7, -1, -1):
            v.append(b >> i & 1)
    return v


def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n
# returns hidden payload based on password

def calculate_size(size_pixels_searchspace):
    size_bytes = []
    for i, byte in enumerate(size_pixels_searchspace):
        size_bytes.append(byte[0])
        if i!=5:        # ignore the last 2 bytes in the last size pixel as they don't belong to the size mapping
            size_bytes.append(byte[1])
            size_bytes.append(byte[2])
    size_bytes = list(reversed(size_bytes))
    size_bin = []
    for byte in size_bytes:
        for i in range(1, -1, -1):
            size_bin.append(byte >> i & 1)

    size_bin = list(reversed(size_bin))
    size_value = ''
    construct_bin_aux = '0b'
    for i, binn in enumerate(size_bin):
        construct_bin_aux += str(binn)        
        if len(construct_bin_aux)==6:
            # construct size_value
            size_value += str(hex(int(construct_bin_aux,2)))[2:]
            construct_bin_aux = '0b'
    # reverse size_value, byte to byte.
    size_value = size_value[-2:] + size_value[-4:-2] + size_value[-6:-4] + size_value[-8:-6]
    # size in base 10
    size_value = int(size_value,16)
    return size_value

def discover_secret(secret_pixels_searchspace, secret_size):
    bits_to_read = secret_size*8
    parsed_secret_bytes = []
    for i, byte in enumerate(secret_pixels_searchspace):
        if i!=0:        # ignore the last 2 bytes as they don't belong to the size mapping
            parsed_secret_bytes.append(byte[0])
        parsed_secret_bytes.append(byte[1])
        parsed_secret_bytes.append(byte[2])

    # 2 useful bit per byte
    parsed_secret_bytes = parsed_secret_bytes[0:bits_to_read/2]
    # reverse read bytes
    parsed_secret_bytes = list(reversed(parsed_secret_bytes))
    parsed_secret_bin = []
    for byte in parsed_secret_bytes:
        for i in range(1, -1, -1):
            parsed_secret_bin.append(byte >> i & 1)

    secret_value_aux = ''
    secret = ''
    for i, binn in enumerate(parsed_secret_bin):
        secret_value_aux += str(binn)
        if len(secret_value_aux)==8:
            secret += chr(int(secret_value_aux[::-1],2))
            secret_value_aux = ''
    return secret[::-1]




def extract(imgFile, password):
    img = Image.open(imgFile)
    width, height = img.size
    conv = img.convert('RGBA').getdata()
    pixel_list = list(conv)
    initial_pixel = password
    size_pixels_searchspace = pixel_list[initial_pixel:initial_pixel+6]
    secret_size = calculate_size(size_pixels_searchspace)
    #print 'Tamanho: %d' %(secret_size)
    max_info_pixels = (secret_size*8)/6 + 1
    # in the pixel "initial_pixel+5", the G and B bytes still have 4 bits of information
    secret_pixels_searchspace = pixel_list[initial_pixel+5:initial_pixel+5+max_info_pixels]
    secret = discover_secret(secret_pixels_searchspace, secret_size)
    print secret
    
    
def usage(progName):
    print 'Ciber Securanca Forense - Instituto Superior Tecnico / Universidade Lisboa, modified by our group to pwn the original file'
    print 'LSB steganography tool: unhide files based on least significant bits of images.\n'
    print ''
    print 'Usage:'
    print '  %s <img_file> [password]' % progName
    print ''
    print '  The password is optional and must be a number.'
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 1:
        usage(sys.argv[0])
    password = int(sys.argv[2]) % 13 if len(sys.argv) > 2 else 0
    #password = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    extract(sys.argv[1], password)
# okay decompiling compress.pyc
