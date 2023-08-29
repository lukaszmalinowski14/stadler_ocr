from pytesseract import *
import argparse
import cv2
from pathlib import Path
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import *


# BOM path
import typeBOM

# analiza plików
import pdf_to_image
import read_page


###########################################################################################################################
# MAIN
###########################################################################################################################

# test

# read_page.testdf_from_sql()

###########################################################################################################################

# TODO: select directory
# https://stackoverflow.com/questions/11295917/how-to-select-a-directory-and-store-the-location-using-tkinter-in-python
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()


# TODO: Identyfikacja typu BOMu
files, type = typeBOM.list_directory(folder_selected)

if type == 0:
    pdf_to_image.create_temp_directory(folder_selected)
    for file in files:
        # path = folder_selected+"/"+file
        # TODO: zapisanie strony jako obraz
        pdf_to_image.page_to_img(folder_selected, file, type)

    # TODO: analiza OCR obrazów stron

    read_page.list_directory(folder_selected+'/'+'temp_pages')

elif type in (1, 2):
    import tabula_ocr
    print(f"type {type}")
    tabula_ocr.type_one_list_files(folder_selected, type)

# elif type == 2:
#     print("type 2")
