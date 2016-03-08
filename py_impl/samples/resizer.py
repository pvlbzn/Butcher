import os
import sys
from PIL import Image

img = Image.open("input/level_activity_background.png")
print(img.size)

size = img.size[0] / 2, img.size[1] / 2
img.thumbnail(size, Image.ANTIALIAS)
print(img.size)

img.save("out_antialias.png", "PNG")
