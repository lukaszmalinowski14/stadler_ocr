import tabula as tb
import pandas as pd
import re
import os
import PyPDF2
from pathlib import Path
import numpy as np
import sql
import glob

structura = pd.DataFrame(
    columns=['Typ', 'ilosc', 'typ_ilosc', 'Nazwa', 'Rys', 'Material', 'Grubosc', 'Waga', 'Kod', ])


def type_one_list_files(path, type):
    if type == 1:
        pliki = sorted(Path(path).iterdir(), key=os.path.getmtime)

        for file in pliki:
            print(str(file).upper())
            if str(file).upper().endswith('BOM.PDF'):
                stadler_Swiss(str(file))

    if type == 2:
        lista_plikow = []
        krotka_list = os.walk(path)
        # count_folders = 0
        # count_files = 0
        for _ in krotka_list:
            print(_)
            # count_folders += 1
            # Unpacking tuple
            sciezka = _[0]
            lista_folderow = list(_[1])  # Convert generator to a list
            pliki = list(_[2])  # Convert generator to a list

            # Displaying content
            print("Ścieżka:", sciezka)
            print("Lista folderow:", lista_folderow)
            print("Lista plików:", lista_plikow)

            list_of_files = filter(os.path.isfile,
                                   glob.glob(str(_[0]) + '/*'))

            list_of_files = sorted(list_of_files,
                                   key=os.path.getmtime, reverse=True)

            # pliki = sorted(Path(str(_[0])).iterdir(), key=os.path.getmtime)

            count = 0
            for el in list_of_files:
                if str(el).upper().endswith('.PDF'):
                    if count == 0:
                        lista_plikow.append(el)
                    count += 1

        for _ in lista_plikow:
            stadler_more(str(_))


def clear_data(df):

    columns = ['Typ', 'ilosc', 'typ_ilosc',
               'Nazwa', 'Rys', 'Material', 'Grubosc', 'Waga', 'Kod', 'Main']
    print(df)
    df = df[[0, 2, 3, 1, 1, 5, 7, 6, 1, 'Main']]
    df.columns = columns
    main = df.iloc[0]['Main']
    print(df)

    sql.df_to_sql(df, main)


def clear_data_more(df):

    columns = ['Typ', 'ilosc', 'typ_ilosc',
               'Nazwa', 'Rys', 'Material', 'Grubosc', 'Waga', 'Kod', 'Main']
    print(df)
    df = df[[3, 4, 5, 1, 6, 2, 'empty', 'empty', 0, 'Main']]
    df.columns = columns
    print(df)

    sql.df_to_sql(df)


def stadler_Swiss(file):
    # wynikowe df
    df_out = pd.DataFrame(columns=('kod', 'grubosc', 'gatunek'))

    # file = '12676012_deu.pdf'
    reader = PyPDF2.PdfReader(file)
    totalPages1 = len(reader.pages)
    print(totalPages1)
    for page in range(totalPages1):
        box = reader.pages[0].mediabox
        print(f"width: {box.width}")
        print(f"height: {box.height}")
        df = tb.read_pdf(
            file, pages='1', area=(36, 20, 450, 800), pandas_options={'header': True}, stream=True)
        # print(tables)
        # df = tb.read_pdf(_, pages=str(1), area=(
        #     0, 0, 100, 100), pandas_options={'header': None}, stream=True)

        print(df)

        # display each of the dataframes
    wiersz = np.array([])
    tabela = np.empty((0, 8), str)

    for dfs in df:
        print(dfs.size)
        print(dfs)
        # sprawdzenie czy kolumna zawiera "t="
        rows, columns = dfs.shape
        start_index = 2
        for index in range(start_index, rows):
            # zapisanie wiersza do tabeli
            print(dfs.iloc[index][0])
            if not np.isnan(dfs.iloc[index][0]) and len(wiersz) > 0:
                # jesżeli długowsc wiersz ==7 (brak grubosci materialu):
                if len(wiersz) == 7:
                    wiersz = np.append(
                        wiersz, None)
                tabela = np.vstack((tabela, wiersz))
                wiersz = np.array([])

            for col in range(columns):
                cell_val = dfs.iloc[index][col]
                print(type(cell_val))

                # przypisanie indexu 0 dla elementu głownego
                if col == 0 and index == 2 and np.isnan(cell_val):
                    cell_val = 0
                    Main_index = (0, index)
                # przypisanie indexu do zmiennej index
                if col == 0:
                    Pos = cell_val
                print(cell_val)

                if col in (0, 1, 2, 3, 4, 6, 9) and not np.isnan(Pos):
                    if index == 2 and col == 2:
                        cell_val = '1'
                    elif str(cell_val) == 'nan':
                        cell_val = None
                    wiersz = np.append(
                        wiersz, cell_val)
                if col == 4 and np.isnan(Pos):
                    if str(cell_val) == 'nan':
                        cell_val = None
                    wiersz = np.append(
                        wiersz, cell_val)

            # x = (wiersz.shape)[0]
            # if x == 8:

    # zapisanie ostatniego wiersza:

    if len(wiersz) == 7:
        wiersz = np.append(
            wiersz, None)
    tabela = np.vstack((tabela, wiersz))
    data = pd.DataFrame(tabela)
    main = data.iloc[0][1]
    data['Main'] = main
    clear_data(data)

    # if (df[5].str.contains('t=')).any():

    #     # dla jednoliniowego bomu
    #     if len(df.index) < 7:
    #         new_row = pd.Series(
    #             {'kod': df.iloc[3, 1], 'grubosc': df.iloc[5, 5], 'gatunek': df.iloc[3, 8]})
    #     # dla wielo liniowego bomu
    #     else:
    #         new_row = pd.Series(
    #             {'kod': df.iloc[3, 1], 'grubosc': df.iloc[8, 5], 'gatunek': df.iloc[6, 9]})

    #         # print(df.iloc[3, 1])
    #         # print(df.iloc[6, 9])
    #         # print(df.iloc[8, 5])

    #     df_out = append_row(df_out, new_row)
    # print(df_out)


def stadler_anzahl(dfs):
    wiersz = np.array([])
    tabela = np.empty((0, 8), str)
    print("test_stadler_anzahl")
    check_index = 2
    start_index = 2
    rows, columns = dfs.shape
    row_count = 0
    print(dfs)

    for index in range(start_index, rows):
        row_count += 1
        if row_count > 3:
            row_count = 1
        # zapisanie wiersza do tabeli
        print(dfs.iloc[index][0])
        # if not np.isnan(dfs.iloc[index][0]) and len(wiersz) > 0:
        # jesżeli długowsc wiersz ==7 (brak grubosci materialu):

        if row_count == 1:
            if len(wiersz) > 2:
                wiersz = np.append(
                    wiersz, None)
                tabela = np.vstack((tabela, wiersz))
            wiersz = np.array([])

        for col in range(columns):
            cell_val = dfs.iloc[index][col]
            # print(type(cell_val))

            # przypisanie indexu 0 dla elementu głownego
            # if col == 0 and index == check_index and np.isnan(cell_val):
            if col == 0 and index == check_index and str(cell_val) == 'nan':
                cell_val = 0
                Main_index = (0, index)
                wiersz = np.append(
                    wiersz, cell_val)
            # przypisanie indexu do zmiennej index
            if col == 0:
                Pos = cell_val
            print(cell_val)
            elo = 1

            if row_count == 1:
                if col in (3, 7):
                    if str(cell_val) == 'nan':
                        cell_val = None
                    wiersz = np.append(
                        wiersz, cell_val)

            if row_count == 2:
               # if col == 0 and index == 0 and np.isnan(cell_val):
                if col == 2:
                    if str(cell_val) == 'nan':
                        cell_val = None
                    wiersz = np.append(
                        wiersz, cell_val)

            if row_count == 3:
                if col == 3:
                    if str(cell_val) == 'nan':
                        cell_val = None
                    if cell_val != None:
                        wiersz[1] = str(wiersz[1]) + ' ' + cell_val

    # zapisanie ostatniego wiersza:
    if len(wiersz) == 7:
        wiersz = np.append(
            wiersz, cell_val)
        tabela = np.vstack((tabela, wiersz))
    return tabela


def stadler_more(file):
    if file == 'N:/Wsp-Ogol/Backlog_raporty_LMA/Stadler_struktury/12291999\\12075170\\12075170-000-deu.pdf':
        print("test")
    # wynikowe df
    df_out = pd.DataFrame(columns=('kod', 'grubosc', 'gatunek'))

    # file = '12676012_deu.pdf'
    reader = PyPDF2.PdfReader(file)
    totalPages1 = len(reader.pages)
    print(totalPages1)
    for page in range(totalPages1):
        box = reader.pages[0].mediabox
        print(f"width: {box.width}")
        print(f"height: {box.height}")
        df = tb.read_pdf(
            file, pages='1', area=(70, 10, 450, 800), pandas_options={'header': False}, stream=True)
        # df = tb.read_pdf(
        #     file, pages='1', area=(70, 15, 450, 800), pandas_options={'header': False}, stream=True)
        # print(tables)
        # df = tb.read_pdf(_, pages=str(1), area=(
        #     0, 0, 100, 100), pandas_options={'header': None}, stream=True)

        print(df)
        # display each of the dataframes
    wiersz = np.array([])
    tabela = np.empty((0, 8), str)

    for dfs in df:
        print(dfs.size)
        print(dfs)
        # sprawdzenie czy kolumna zawiera "t="

        start_index = 0
        check_index = 1
        # print(dfs.iloc[0][1])
        # informacja o krustszej tabeli:
        material_col = 9
        rows, columns = dfs.shape

        column_names = list(dfs.columns)
        print(column_names)

        if dfs.iloc[0][1] == 'Anzahl':
            stadler_anzahl(dfs)
            continue

        if columns == 7:
            dfs.insert(loc=0, column='Pos1', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=3, column='Meng', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=4, column='ME', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=7, column='Vorzug', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=10, column='Hersteller', value=[
                       'nan' for i in range(dfs.shape[0])])
            print(dfs)

        if columns == 8:
            dfs.insert(loc=0, column='Pos1', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=3, column='Meng', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=4, column='ME', value=[
                       'nan' for i in range(dfs.shape[0])])
            dfs.insert(loc=7, column='Vorzug', value=[
                       'nan' for i in range(dfs.shape[0])])
            print(dfs)

        rows, columns = dfs.shape

        if dfs.iloc[0][8] == 'Bemerkung':
            print("krótka")
            material_col = 8

        if dfs.iloc[0][1] == 'PLM-Nr.':
            start_index = 1
            check_index = 2
        elif dfs.iloc[1][1] == 'PLM-Nr.':
            start_index = 2
            check_index = 3
        row_count = 0
        for index in range(start_index, rows):
            row_count += 1
            if row_count > 3:
                row_count = 1

             # sprawdzenie poprawnej kolejnosci wierszy
            if row_count == 1 and str(dfs.iloc[index][1]) == 'nan':
                row_count -= 1
                continue

            # zapisanie wiersza do tabeli
            print(dfs.iloc[index][0])
            # if not np.isnan(dfs.iloc[index][0]) and len(wiersz) > 0:
            # jesżeli długowsc wiersz ==7 (brak grubosci materialu):

            if row_count == 1:
                if len(wiersz) > 2:
                    wiersz = np.append(
                        wiersz, None)
                    tabela = np.vstack((tabela, wiersz))
                wiersz = np.array([])

            for col in range(columns):
                cell_val = dfs.iloc[index][col]
                # print(type(cell_val))

                # przypisanie indexu 0 dla elementu głownego
                # if col == 0 and index == check_index and np.isnan(cell_val):
                if col == 0 and index == check_index and str(cell_val) == 'nan':
                    cell_val = 0
                    Main_index = (0, index)
                # przypisanie indexu do zmiennej index
                if col == 0:
                    Pos = cell_val
                print(cell_val)
                elo = 1

                if row_count == 1:
                    if col in (1, 5, material_col):
                        if str(cell_val) == 'nan':
                            cell_val = None
                        print(type(cell_val))
                        if col == 1 and str(type(cell_val)) == "<class 'numpy.float64'>":
                            cell_val = cell_val.astype(np.int64)
                            cell_val = str(cell_val)
                        wiersz = np.append(
                            wiersz, cell_val)

                if row_count == 2:
                   # if col == 0 and index == 0 and np.isnan(cell_val):
                    if col == 0 and index == 0 and str(cell_val) == 'nan':
                        cell_val = 0
                        wiersz = np.append(
                            wiersz, cell_val)
                    elif col in (0, 3, 4):
                        if col == 3 and str(cell_val) == 'nan':
                            cell_val = '1'
                            # przypisanie ilosc 1 i STK dla gdt puste (pierwszy element na liscie)
                        if col == 4 and str(cell_val) == 'nan':
                            cell_val = 'STK'
                        if str(cell_val) == 'nan':
                            cell_val = None
                        wiersz = np.append(
                            wiersz, cell_val)

                if row_count == 3:
                    if col == 5:
                        if str(cell_val) == 'nan':
                            cell_val = None
                        if cell_val != None:
                            if str(wiersz[1]) == 'None':
                                wiersz[1] = cell_val
                            else:
                                wiersz[1] = str(wiersz[1]) + ' ' + cell_val
                    elif col == material_col:
                        if str(cell_val) == 'nan':
                            cell_val = None
                        if cell_val != None:
                            if str(wiersz[2]) == 'None':
                                wiersz[2] = cell_val
                            else:
                                wiersz[2] = str(wiersz[2]) + ' ' + cell_val
                    elif col == 1:
                        if str(cell_val) == 'nan':
                            cell_val = None
                        wiersz = np.append(
                            wiersz, cell_val)

                # if row_count == 1:
                #     print("wiersz 1")
                #     if col in (0, 4, 9):
                #         if str(cell_val) == 'nan':
                #             cell_val = None
                #         # Zapisanie jednostki sztuk dla główngo prduktu
                #         # if col == 4 and cell_val == None:
                #         #     cell_val = 'STK'
                #         wiersz = np.append(
                #             wiersz, cell_val)
                # if row_count == 2:
                #     if col in (0, 3):
                #         if col == 3:
                #             if str(cell_val) == 'nan':
                #                 wiersz = np.append(
                #                     wiersz, '1')
                #                 wiersz = np.append(
                #                     wiersz, 'STK')
                #             else:
                #                 x = cell_val.split(" ")
                #                 wiersz = np.append(
                #                     wiersz, x[0])
                #                 wiersz = np.append(
                #                     wiersz, x[1])
                #         if col == 0:
                #             if str(cell_val) == 'nan':
                #                 cell_val = None
                #                 if col == 0 and cell_val == None:
                #                     cell_val = '0'
                #             wiersz = np.append(
                #                 wiersz, cell_val)
                # if row_count == 3:
                #     if col in (0, 4, 8):
                #         if col == 4:
                #             if str(cell_val) != 'nan':
                #                 wiersz[1] = wiersz[1]+''+cell_val
                #         if col == 8:
                #             if str(cell_val) != 'nan':
                #                 wiersz[2] = str(wiersz[2])+''+cell_val
                #         else:
                #             if str(cell_val) == 'nan':
                #                 cell_val = None
                #             wiersz = np.append(
                #                 wiersz, cell_val)

                # if col in (0, 1, 2, 3, 4, 6, 9) and str(Pos) != 'nan':
                #     if str(cell_val) == 'nan':
                #         cell_val = None
                #     # Zapisanie jednostki sztuk dla główngo prduktu
                #     if col == 2 and cell_val == None:
                #         cell_val = 'STK'
                #     wiersz = np.append(
                #         wiersz, cell_val)
                # if col == 4 and str(Pos) == 'nan':
                #     if str(cell_val) == 'nan':
                #         cell_val = None
                #     wiersz = np.append(
                #         wiersz, cell_val)

            # x = (wiersz.shape)[0]
            # if x == 8:

    # zapisanie ostatniego wiersza:
    if len(wiersz) == 7:
        wiersz = np.append(
            wiersz, cell_val)
        tabela = np.vstack((tabela, wiersz))
    data = pd.DataFrame(tabela)
    print(data)
    rows, columns = data.shape

    if (rows > 0 and columns > 0):
        main = data.iloc[0][0]
        if str(main) == 'None':
            print("sfgfg")
        pusty = None
        data['Main'] = main
        data['empty'] = pusty
        clear_data_more(data)

    # if (df[5].str.contains('t=')).any():

    #     # dla jednoliniowego bomu
    #     if len(df.index) < 7:
    #         new_row = pd.Series(
    #             {'kod': df.iloc[3, 1], 'grubosc': df.iloc[5, 5], 'gatunek': df.iloc[3, 8]})
    #     # dla wielo liniowego bomu
    #     else:
    #         new_row = pd.Series(
    #             {'kod': df.iloc[3, 1], 'grubosc': df.iloc[8, 5], 'gatunek': df.iloc[6, 9]})

    #         # print(df.iloc[3, 1])
    #         # print(df.iloc[6, 9])
    #         # print(df.iloc[8, 5])

    #     df_out = append_row(df_out, new_row)
    # print(df_out)
