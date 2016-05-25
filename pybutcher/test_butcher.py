import pytest
import os
import butcher

# Needed for test env
from PIL import Image


# Create test dir and test imges
def create_test_env(n, w, h):
    ''' Create testing environment (folder and images). Return test folder path. '''
    path = os.path.join(os.getcwd(), 'testenv')
    if not os.path.isdir(path):
        os.mkdir(path)
    while n > 0:
        img = Image.new('RGB', (w, h))
        name = 'img{}.png'.format(str(n))
        img.save(os.path.join(path, name), "PNG")
        n -= 1
    return path


def cleanup(path):
    ''' Clean project from test env. Should be executed by the last test. '''
    import shutil
    if os.path.isdir(path):
        # Nope:
        # os.system("rm -rf " + path)
        shutil.rmtree(path)


def test_files():
    path = create_test_env(2, 250, 250)
    assert butcher.files(path) == ["img1.png", "img2.png"]


def test_get_sizes():
    path = os.path.join(os.getcwd(), 'testenv')
    m = Image.open(os.path.join(path, 'img1.png'))
    assert butcher.get_sizes(m, 'mdpi', ['mdpi']) == {'mdpi': (250.0, 250.0)}


def test_downscale():
    path = os.path.join(os.getcwd(), 'testenv')
    m = Image.open(os.path.join(path, 'img1.png'))
    butcher.check_dirs(os.path.join(path, 'drawable-'), ['mdpi'])
    butcher.downscale(m, {'mdpi': (250.0, 250.0)}, 'img1.png', 'testenv')
    cleanup(path)
