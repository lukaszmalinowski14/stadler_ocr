from pytesseract import *
import argparse
import cv2
from pathlib import Path
import pandas as pd
import numpy as np
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from PIL import Image
from pathlib import Path
import os
# import sql
# import openpyxl
# import matplotlib.image

# table = pd.DataFrame(columns=['main', 'typ', 'Kode', 'Nazwa', 'ilosc', 'IDop'])
df = pd.DataFrame()
structura = pd.DataFrame(
    columns=['Typ', 'ilosc', 'typ_ilosc', 'Nazwa', 'Rys', 'Material', 'Grubosc', 'Waga', 'Kod', 'Uwagi'])


def clear_structura():
    global structura
    structura = pd.DataFrame(
        columns=['Typ', 'ilosc', 'typ_ilosc', 'Nazwa', 'Rys', 'Material', 'Grubosc', 'Waga', 'Kod', 'Uwagi'])

    global df
    df = pd.DataFrame()


def testdf_from_sql():
    global structura
    import psycopg2
    from sqlalchemy import create_engine
    conn_string = 'postgresql://testdbuser:Xai7aer7pu@10.1.5.30/pimstalnew'

    db = create_engine(conn_string)
    conn = db.connect()
    conn1 = psycopg2.connect(
        database="pimstalnew",
        user='testdbuser',
        password='Xai7aer7pu',
        host='10.1.5.30',
        port='5432'
    )

    conn1.autocommit = True
    cursor = conn1.cursor()

    # test read sql to df
    a = pd.read_sql_query('select * from meteurosystem.pandas_df', con=db)

    rows, columns = a.shape

    # print("test")
    # for index, row in a.iterrows():
    #     print(row["1"])

    # data = {
    #     "firstname": ["Sally", "Mary", "John"],
    #     "age": [50, 40, 30]
    # }

    # list = ["Emma", 100]

    # df = pd.DataFrame(data)

    # df.loc[len(df)] = list
    # print(df)

    # index = 0
    # col = 0

    ################################


def ocr_file():
    images = cv2.imread("table.png")
    rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

    # XXXXXXXXXXXXXXXXXXXXXXXXXX
    # lines_y = [10, 80, 140, 210, 280, 355, 420, 492, 560,
    #            630, 690, 768, 830, 905, 960, 1040, 1100]

    # lines_x = [30, 120, 220, 510, 580, 950, 1500, 1820, 1950]
    lines_y = [10, 80, 150, 220, 280, 355, 420, 492, 560,
               630, 690, 768, 830, 905, 960, 1040, 1100]

    lines_x = [30, 120, 220, 510, 580, 950, 1465, 1820, 1950]

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
                wiersz, czytanie_wartosci_komorki(x, y, w, h, count_x, rgb))
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
            # print("#################")
            # print(pd.DataFrame(tabela))
        if count_y > 6 and all(element == '' for element in wiersz):
            # print("test")
            break
        wiersz = np.array([])

    ###############################################################
    data = pd.DataFrame(tabela)
    # print("XXXXXXXXXXXXXXXXXXXXXXX")
    # print(data)
    # After all, we will show the output image
    cv2.imshow("Image", images)
    cv2.waitKey(0)

    put_to_table(data)


def list_directory(path):

    pliki = sorted(Path(path).iterdir(), key=os.path.getmtime)

    for file in pliki:
        print(file)
        if (analize_page(str(file))):
            ocr_file()

    # zapisanie ostatniej skladowej
    clear_data()


def analize_page(file):
    # read your file
    # file = r'C:/Python/ocr_2/page2.jpg'
    if file.endswith('.png'):
        ######
        im = Image.open(file)
        width, height = im.size
        if width == 2339 and height == 1653:
            im1 = im.crop((0, 165, 2250, 1280))
            im1.show()
            im1.save("table.png")
            return True
    return False


def czytanie_wartosci_komorki(x, y, w, h, kolumna, rgb):
    import pytesseract
    conf1 = "--psm 7 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZl-g.n0123456789"
    conf2 = '--psm 7 --oem 1 -c tessedit_char_whitelist=X0123456789,.'

    if kolumna in (0, 1, 2, 7):
        conf = conf2
    else:
        conf = conf1
    finalimg = rgb[y:y+h, x:x+w]
    # finalimg.show()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    # border = cv2.copyMakeBorder(
    #     finalimg, 2, 2, 2, 2,   cv2.BORDER_CONSTANT, value=[255, 255])
    resizing = cv2.resize(finalimg, None, fx=2,
                          fy=2, interpolation=cv2.INTER_CUBIC)
    # dilation = cv2.dilate(resizing, kernel, iterations=1)
    # erosion = cv2.erode(dilation, kernel, iterations=1)
    cv2.imwrite(str(Path.cwd())+"/resize.png", resizing)
    out = pytesseract.image_to_string(resizing)

    # PSM 3 dla złozonych i poj wyrazów
    ##
    out = pytesseract.image_to_string(
        resizing, config=conf)
    # if (len(out) == 0):

    # filtrowanie błędnych wyników
    if kolumna in (4, 5) and len(out) < 4:
        out = ""

    # print(len(out))
    # print(f"odczytany teskt to {out}")
    out = out.replace('\n', '')
    return out


def korekta(x, y, w, h, kolumna):
    if kolumna in (0, 1, 2, 3, 6, 7):
        x += 5
        y += 5
        w -= 10
        h -= 10
    elif kolumna == 4:
        x += 5
        y += 5
        w -= 7
        h -= 8
    elif kolumna == 5:
        x += 5
        y += 5
        w -= 2
        h -= 3

    return x, y, w, h


def clear_data():
    global df
    global structura
    # Drop rows with any empty cells
    # df.dropna(
    #     axis=0,
    #     how='all',
    #     subset=None,
    #     inplace=True
    # )
    # print(df)
    rows, columns = df.shape

    row = []
    for index in range(rows):
        for col in range(columns):
            if col == 1:
                continue
            cell_val = df.iloc[index][col]
            if index % 2 == 0:
                if cell_val != '':
                    row.append(cell_val)
                else:
                    row.append(None)
                # dodanie klumny na grubosc materialu
                if col == 6:
                    row.append(None)
            if index % 2 == 1 and col == 5:
                if cell_val != '':
                    row.append(cell_val)
                else:
                    row.append(None)

        if index % 2 == 1:
            if index == 1 and row[1] == 'X':
                row[0] = '0'
                row[4] = 'X'
                main = row[8]
            print(row)
            if not all(element == None for element in row):
                structura.loc[len(structura)] = row
                # else:
                #     print("ERROR")
            row = []
    structura['Main'] = main
    print(structura)

    sql.df_to_sql(structura, main)
    clear_structura()

    # insert to db


def put_to_table(tab_temp):
    global df
    print(tab_temp.iloc[0, 2])
    if tab_temp.iloc[0, 2] == 'X' and not df.empty:
        # uporządkuj dane
        clear_data()
        # zapisz dane do bazydanych
        # wyczysc global df

        print("test")

    # table = np.empty((0, 8), str)
    # df_temp = tab_temp
    if df.empty:
        df = tab_temp
    else:
        df = pd.concat([df, tab_temp], ignore_index=True)
    # table = np.vstack((table, tab_temp))
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # data = pd.DataFrame(table)
    print(df)

    # df_to_sql(df)
