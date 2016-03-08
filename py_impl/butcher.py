import os, sys
from PIL import Image

import time


def downscale_size(img, scale):
    nsize = img.size
    xsize = nsize[0] * scale
    ysize = nsize[1] * scale
    return (int(xsize), int(ysize))

def downscale(address, scale, f):
    with Image.open(address) as img:
        size = downscale_size(img, scale)
        name = "%s_%.2f.png" % (f, float(scale))
        fname = os.path.abspath("output") + '/' + name
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(fname, "PNG")

def input():
    return os.listdir("input")

def do():
    stime = time.time()
    flist = input()
    for f in flist:
        downscale("input/" + f, .5, f)
    print("%s seconds" % (time.time() - stime))

if __name__ == "__main__":
    do()
