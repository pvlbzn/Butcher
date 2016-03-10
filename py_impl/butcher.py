import os
import sys
import time

from PIL import Image
from pathlib import Path

DPI = ['ldpi', 'mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']
SCALES = {"ldpi": .75, "mdpi": 1.0, "hdpi": 1.5,
        "xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}

def files():
    afiles = os.listdir("input")
    sfiles = []
    for f in afiles:
        if f[len(f)-4:] == ".png":
            sfiles.append(f)
    return sfiles

def read_args():
    # Take a first argument, which has to be
    return sys.argv[1]

def get_sizes(img, dpi, dpi_range):
    size = img.size
    # Downscale size to mdpi
    print(size[0], size[1])
    mdpi_w = size[0] / SCALES[dpi]
    mdpi_h = size[1] / SCALES[dpi]
    sizes = {}
    for scale in SCALES:
        if scale in dpi_range:
            w = mdpi_w * SCALES[scale]
            h = mdpi_h * SCALES[scale]
            sizes[scale] = (w, h)
    return sizes

def downscale(img, sizes, name):
    for key in sizes:
        folder = '/' + "drawable-" + key + '/'
        fname = os.path.abspath("output") + folder + name
        print("Saving file {0} in {1}".format(name, fname))
        print(key, sizes[key])
        # Copy img. Otherwise one image will be croped len(sizes) times.
        i = img.copy()
        i.thumbnail(sizes[key], Image.ANTIALIAS)
        i.save(fname, "PNG")
        i.close()

def check_dirs(sizes):
    for key in sizes:
        # TODO: Use different path generation.
        dir = Path("output/drawable-" + key)
        if not dir.exists():
            dir.mkdir()

def main():
    flist = files()
    user_dpi = read_args()
    # Filter out DPI that higher than user's DPI.
    dpi_range = DPI[:DPI.index(user_dpi) + 1]
    for fname in flist:
        addr = "input/" + fname
        with Image.open(addr) as img:
            sizes = get_sizes(img, user_dpi, dpi_range)
            check_dirs(sizes)
            print("Should be once!")
            # Check directories for DPIs which will be used.
            downscale(img, sizes, fname)

if __name__ == '__main__':
    main()
