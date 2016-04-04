import os
import sys

from PIL import Image

DPI = ["ldpi", "mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
SCL = {"ldpi": .75, "mdpi": 1.0, "hdpi": 1.5,
        "xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}

def files(folder):
    """Fetches files.
    Fetches files from input folder and filter them by file prefix.
    Args:
        folder (str): Name of the folder with images.
    Returns:
        List of the image files.
    """
    afiles = os.listdir(folder)
    sfiles = []
    for f in afiles:
        # Can be used feature from stdlib, but this way is ok for cuurent impl.
        if f[len(f)-4:] == ".png":
            sfiles.append(f)
    return sfiles

def read_args():
    """Return first arg, which should be DPI name."""
    return sys.argv[1]

def get_sizes(img, dpi, dpi_range):
    """Create sizes in which the user image(s) should be converted.
    Args:
        img (Image): Already opened image which should be processed.
        dpi (string): Original size DPI. Was provided by the user.
        dpi_range (list): List of DPIs from user DPI to lowest DPI.
    Returns:
        Dictionary where DPI (string) is a key and tuple of width, height
        (float). Example: {'DPI': (W, H), ... }
    """
    size = img.size
    # Downscale size to mdpi for convinience.
    mdpi_w = size[0] / SCL[dpi]
    mdpi_h = size[1] / SCL[dpi]
    sizes = {}
    for scale in SCL:
        if scale in dpi_range:
            w = mdpi_w * SCL[scale]
            h = mdpi_h * SCL[scale]
            sizes[scale] = (w, h)
    return sizes

def downscale(img, sizes, name, dir):
    """Downscale image.
    Iterates over 'sizes' dictionary entries, where key is a DPI and a value
    is a tuple with width, height. While iterating over entries, its shrinks
    images to the size of the entry tuple and saves an output to the folder
    with name 'drawable-[DPI]'.
    Args:
        img (Image): Already opened image which slould be processed.
        sizes (dict): Dictionary {'DPI': (H, W), ... }
        name (string): Original filename.
    """
    for key in sizes:
        folder = '/' + "drawable-" + key + '/'
        fname = os.path.abspath(dir) + folder + name
        print("Saving file {0}({1}) as w:{2} h:{3}.".format(name, img.size,
            sizes[key][0], sizes[key][1]))
        # Copy img. Otherwise one image will be croped len(sizes) times.
        i = img.copy()
        i.thumbnail(sizes[key], Image.ANTIALIAS)
        i.save(fname, "PNG")
        i.close()

def check_dirs(output_dir, sizes):
    """Check is needed directories exists.
    If not - create it.
    Args:
        output_dir (string): Name of the output folder.
        sizes (dict): Dictionary of the sizes.
    """
    for key in sizes:
        dir = output_dir + key
        if not os.path.isdir(dir):
            os.mkdir(dir)

def main():
    flist = files("input")
    output_dir = os.path.join(os.getcwd(), 'output', "drawable-")
    user_dpi = read_args()
    # Filter out DPI that 'bigger' than user's DPI.
    dpi_range = DPI[:DPI.index(user_dpi) + 1]
    for fname in flist:
        addr = "input/" + fname
        with Image.open(addr) as img:
            sizes = get_sizes(img, user_dpi, dpi_range)
            check_dirs(output_dir, sizes)
            downscale(img, sizes, fname, "output")

if __name__ == '__main__':
    main()
