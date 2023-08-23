from pytesseract import *
import argparse
import cv2
from pathlib import Path
import pandas as pd
import numpy as np


images = cv2.imread("table.png")
rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)


# XXXXXXXXXXXXXXXXXXXXXXXXXX
lines_y = [10, 80, 140, 210, 280, 355, 420, 492, 560,
           630, 690, 768, 830, 905, 960, 1040, 1100]

lines_x = [30, 120, 220, 510, 580, 950, 1500, 1820, 1950]

# wyznaczenie punktów przeciecia linni
count_x = 0
count_y = 0


wiersz = np.array([])
tabela = np.empty((0, 8), str)


for y_line in lines_y:
    for x_line in lines_x:
        x, y = (x_line, y_line)
        if count_x < 8:
            w = lines_x[count_x+1]-x_line
        else:
            continue
        if count_y < 16:
            h = lines_y[count_y+1]-y_line
        else:
            continue

        (x, y, w, h) = korekta(x, y, w, h, count_x)
        wiersz = np.append(
            wiersz, czytanie_wartosci_komorki(x, y, w, h, count_x))
        cv2.rectangle(images,
                      (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)

        # UMIESZCZENIE WARTOSCI W TABELI

        # POKAŻ ZAZNACZONY BOX
        # cv2.imshow("Image", images)
        # cv2.waitKey(0)
        count_x += 1
    count_y += 1
    count_x = 0

    x = (wiersz.shape)[0]
    if x == 8:
        tabela = np.vstack((tabela, wiersz))
        print("#################")
        print(pd.DataFrame(tabela))
    wiersz = np.array([])


###############################################################

# After all, we will show the output image
cv2.imshow("Image", images)
cv2.waitKey(0)
