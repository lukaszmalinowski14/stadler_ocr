# doc
# https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/
# https://www.geeksforgeeks.org/create-a-directory-in-python/
# import module
from pdf2image import convert_from_path
from pathlib import Path
# importing os module
import os
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as msb
import shutil

# mode
mode = 0o666


def create_temp_directory(path):
    # usuniecie folderu na plii stron jezeli istnieje
    # https://stackoverflow.com/questions/43765117/how-to-check-existence-of-a-folder-with-python-and-then-remove-it
    dirpath = Path(path) / 'temp_pages'
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    os.mkdir(path+'/temp_pages', mode)


def count_files(dir_path):
    count = 0
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count


def page_to_img(path, file, type):
    # Store Pdf with convert_from_path function
    images = convert_from_path(file)
    print(f"file: {file} pages: {len(images)}")
    if len(images) < 4 or type == 0:
        cnt_files = count_files(path+'/temp_pages/')

        for i in range(len(images)):

            # Save pages as images in the pdf
            images[i].save(path+'/temp_pages/'+'page' +
                           str(cnt_files+i+1) + '.png', 'PNG')
