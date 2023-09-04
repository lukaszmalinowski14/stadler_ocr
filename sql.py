import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import delete


def df_to_sql(df, main):
    # import packages

    # df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    # df.rename(columns={'1': 'a', '2': 'b', '3': 'c',
    #                    '4': 'd', '5': 'e', '6': 'f', '7': 'g'}, inplace=True)

    print(df)
    # establish connections
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

    # delete data from table if exists
    # delete
    delete = 'DELETE FROM meteurosystem.pandas_df WHERE "Main" ='+"'"+main+"'"
    # dele = meteurosystem.pandas_df.delete().where(meteurosystem.pandas_df.c."Main" == main)
    cursor.execute(delete)

    # with db.connect() as connection:
    #     result = connection.execute(
    #         text("DELETE FROM [meteurosystem].[pandas_df] WHERE ['Main'] ="+main))
    #     connection.commit()
    #     print(
    #         f"Deleted {result.rowcount} row(s) from ")

    # drop table if it already exists
    # cursor.execute('drop table if exists meteurosystem.pandas_df')

    # sql = '''CREATE TABLE meteurosystem.pandas_df(a text ,
    # b text ,c text,d text,e text,f text,g text,h text);'''

    # cursor.execute(sql)

    # # import the csv file to create a dataframe
    # data = pd.read_csv("airlines_final.csv")

    # data = data[["id", "day", "airline", "destination"]]
    # # Create DataFrame
    # print(data)

    # converting data to sql

    df.to_sql('pandas_df', conn, schema='meteurosystem',
              if_exists='append', index=False)

    # fetching all rows
    # sql1 = '''select * from meteurosystem.pandas_df;'''
    # cursor.execute(sql1)
    # for i in cursor.fetchall():
    #     print(i)

    conn1.commit()
    conn1.close()
