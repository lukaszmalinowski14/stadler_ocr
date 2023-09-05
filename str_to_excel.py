from openpyxl import Workbook
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import simpledialog
import psycopg2
import pandas as pd
from subprocess import Popen
from openpyxl.utils.dataframe import dataframe_to_rows


df_zakup = pd.DataFrame(
    columns=['Dot. indeksu', 'Nazwa', 'Dostawca', 'ilosc na sztuke', 'cena za sztuke', 'Wartosc', 'LT(dni)', 'opis/uwagi'])
df_struktura = pd.DataFrame(
    columns=['Lp', 'Kod', 'Kod nadrzedny', 'Rysunek', 'Rewizja', 'ilosc na projekt', 'ilosc na dostawe', 'ilosc detalu na zlożenie', 'Gatunek', '#'])


def select_kod(kod, df=pd.DataFrame(), pos=0):
    conn_string = 'postgresql://testdbuser:Xai7aer7pu@10.1.5.30/pimstalnew'
    db = create_engine(conn_string)
    conn = db.connect()
    sql_kod = '''SELECT * from meteurosystem.str_kody(%s)'''
    df = pd.read_sql_query(
        sql_kod, con=conn, params=(kod,))

    return df


def select_lki_zak(kod, df=pd.DataFrame(), pos=0):
    conn_string = 'postgresql://testdbuser:Xai7aer7pu@10.1.5.30/pimstalnew'
    db = create_engine(conn_string)
    conn = db.connect()
    sql_lka_zakup = '''SELECT * from meteurosystem.str_lki_zakup(%s)'''
    df = pd.read_sql_query(
        sql_lka_zakup, con=conn, params=(kod,))

    return df


def iterate(df):
    for index, row in df.iterrows():
        print(df)

        # zapisanie do struktury kolejnych elementów:
        if index > 0:
            prepare_main_row(df.iloc[index-1])

        # sprawdzenie elementów zakupowych i L-ek
        df_temp = select_lki_zak(row[8])
        # jeżeli są elementy zakupowe dodanie do listy df_zakup
        ######

        # dla Elek dopisanie gru
        Lki = df_temp.query('typ == 300 and nazwa.str.contains("Blech")')
        print(Lki)
        rows, columns = Lki.shape
        if rows > 0:
            edit_Lka(Lki.iloc[0])

        # elementy zakupowe:
        zakup = df_temp.query(
            'typ == 300 and nazwa.str.contains("Blech")== False')
        print(zakup)
        rows, columns = zakup.shape
        if rows > 0:
            edit_zakup(zakup.iloc[0])

        # sprawdzenie czy element nie ma elementów zależnych:
        df_skl = select_kod(row[8])
        df_skl = df_skl.query(
            'typ >0')
        print(df_skl)


def edit_Lka(df):
    global df_struktura
    # print(df_struktura.loc[len(df_struktura), 'Kod'])
    # print(df_struktura.loc[len(df_struktura)-1, 'Kod'])
    grubosc = str(df[6])[2:]
    df_struktura.loc[len(df_struktura)-1, ['#']] = grubosc

    print(df_struktura)


def edit_zakup(df):
    global df_zakup
    print(df)
    row = []
    row.append(df[9])
    row.append(df[3])
    row.append(None)
    row.append(df[1])
    row.append(None)
    row.append(None)
    row.append(None)
    uwagi = None

    if str(df[5]) != 'None' and str(df[6]) != 'None':
        uwagi = str(df[5]) + '; ' + str(df[6])
    elif str(df[5]) != 'None':
        uwagi = str(df[5])
    elif str(df[6]) != 'None':
        uwagi = str(df[6])
    row.append(uwagi)

    df_zakup.loc[len(df_zakup)] = row

    print(df_zakup)


def prepare_main_row(df):
    global df_struktura
    print(df)
    row = []
    rows, columns = df_struktura.shape
    # for index, row_val in df.iterrows():

    row.append(rows+1)
    row.append(df[8])
    if df[8] == df[9]:
        row.append(None)
    else:
        row.append(df[9])
    row.append(df[4])
    row.append(None)
    row.append(None)
    row.append(None)
    if df[8] == df[9]:
        row.append(None)
    else:
        row.append(df[1])
    row.append(df[5])
    row.append(df[6])

    df_struktura.loc[len(df_struktura)] = row

    print(df_struktura)


def excel_str():
    global df_struktura
    global df_zakup

    # utworenie okna dilogowego tkinter
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    USER_INP = simpledialog.askstring(title="Struktura",
                                      prompt="Podaj kod towaru:")

    # pobranie danych glownego klucza
    df = select_kod(USER_INP)
    # dodanie wpisu do struktury dla elementu głównego:
    prepare_main_row(df.iloc[0])
    for index, row in df.iterrows():
        print(df)

        # zapisanie do struktury kolejnych elementów:
        if index > 0:
            prepare_main_row(df.iloc[index])

        # sprawdzenie elementów zakupowych i L-ek
        df_temp = select_lki_zak(row[8])
        # jeżeli są elementy zakupowe dodanie do listy df_zakup
        ######

        # dla Elek dopisanie gru
        Lki = df_temp.query('typ == 300 and nazwa.str.contains("Blech")')
        print(Lki)
        rows, columns = Lki.shape
        if rows > 0:
            edit_Lka(Lki.iloc[0])

        # elementy zakupowe:
        zakup = df_temp.query(
            'typ == 300 and nazwa.str.contains("Blech")== False')
        print(zakup)
        rows, columns = zakup.shape
        if rows > 0:
            edit_zakup(zakup.iloc[0])

        # sprawdzenie czy element nie ma elementów zależnych:
        if index > 0:
            df_skl = select_kod(row[8])
            df_skl = df_skl.query(
                'typ >0')
            print(df_skl)
            # df = pd.concat([df, df_skl], ignore_index=True)
            rows, columns = df_skl.shape
            if rows > 0:
                iterate(df_skl)

    print(df_struktura)
    # df_struktura.to_csv("struktura.csv")
    # df_zakup.to_csv("zakupy.csv")
    create_excel(df_struktura, 'struktura.xlsx')
    create_excel(df_zakup, 'zakupy.xlsx')

    print("KONIEC")


def create_excel(df, file_name):
    # utworzenie workbooka excela
    wb = Workbook()
    ws = wb.active

    rows = dataframe_to_rows(df, index=False)
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    wb.save(file_name)
