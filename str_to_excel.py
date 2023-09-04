from openpyxl import Workbook
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import simpledialog
import psycopg2
import pandas as pd


def excel_str():
    # utworzenie workbooka excela
    wb = Workbook()
    ws = wb.active

    # utworenie okna dilogowego tkinter
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    USER_INP = simpledialog.askstring(title="Struktura",
                                      prompt="Podaj kod towaru:")

    conn_string = 'postgresql://testdbuser:Xai7aer7pu@10.1.5.30/pimstalnew'
    db = create_engine(conn_string)
    conn = db.connect()

    df = pd.read_sql_query(
        '''SELECT * from meteurosystem.str_kody('''+USER_INP'''+"')''', con=conn)

    print(df)
