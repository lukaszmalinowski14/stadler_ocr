# import csv
# import cv2
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from PIL import Image
from pathlib import Path
import openpyxl
import matplotlib.image


def analize_page():
    # read your file
    # file = r'C:/Python/ocr_2/page2.jpg'
    file = r'C:/Python/ocr_2/page3.jpg'

    ######
    im = Image.open(file)
    width, height = im.size

    im1 = im.crop((0, 165, 2250, 1280))
    im1.show()
    im1.imsave("table.png")
