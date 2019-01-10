from PIL import Image
import numpy as np
from pyimago import imago, FILTER

fp = 'examples/test_image.png'
print("Version", imago.version())
print("Sid", imago.sid)
img = Image.open(fp)

imago.load_image_from_file(fp)
imago.set_filter(FILTER.prefilter_basic)
imago.filter_image()
imago.recognize()
mol = imago.get_mol_text()
print(mol)


if __name__ == '__main__':
    pass