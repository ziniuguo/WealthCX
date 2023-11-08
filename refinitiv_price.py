import os

import mysql.connector
import refinitiv.data as rd
import pandas as pd
import csv
from datetime import datetime, timedelta


def populate(ric):
    pd.set_option('display.max_columns', None)
    os.environ["RD_LIB_CONFIG_PATH"] = "./Configuration"
    rd.open_session()

    # columns = get_RIC.get_ric()
    # print('columns:'+columns[0])

    today = datetime.now().date()
    attempts = 0

    while attempts < 30:
        yesterday = today - timedelta(days=1)
        print("Today's date:", today.strftime('%Y-%m-%d'))
        print("Yesterday's date:", yesterday.strftime('%Y-%m-%d'))
        a = rd.get_history(universe=ric, start=yesterday, end=today)
        b = pd.DataFrame(a)
        if len(b) != 0:
            break
        else:
            today = today - timedelta(days=1)

    b.to_csv('refinitiv.csv', index=True)  # index=False 用于不保存行索引

    rd.close_session()

    config = {
        "user": "doadmin",
        "password": "AVNS_tO45HWZ7rqlgDO7DoU-",
        "host": "db-mysql-sgp1-25924-do-user-14729808-0.b.db.ondigitalocean.com",
        "port": 25060,
        "database": "wealthcx",
    }

    # Establish a MySQL connection and create a cursor

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQL commands
    drop = """DROP TABLE IF EXISTS refinitiv"""
    cursor.execute(drop)
    conn.commit()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS refinitiv (
        Idx BIGINT PRIMARY KEY ,
        Date DATE,
        TRDPRC_1 DOUBLE,
        HIGH_1 DOUBLE,
        LOW_1 DOUBLE,
        ACVOL_UNS BIGINT,
        OPEN_PRC DOUBLE,
        BID DOUBLE,
        ASK DOUBLE,
        TRNOVR_UNS BIGINT,
        VWAP DOUBLE,
        BLKCOUNT BIGINT,
        BLKVOLUM BIGINT,
        NUM_MOVES BIGINT,
        TRD_STATUS BIGINT,
        SALTIM BIGINT,
        NAVALUE VARCHAR(255)
    )
    """

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    cursor = conn.cursor()

    # Read the CSV file and insert data row by row
    i = 0
    with open('refinitiv.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            cursor.execute("""
                INSERT INTO refinitiv
                (Idx,Date,TRDPRC_1,HIGH_1,LOW_1,ACVOL_UNS,OPEN_PRC,BID,ASK,TRNOVR_UNS,VWAP,BLKCOUNT,BLKVOLUM,NUM_MOVES,TRD_STATUS,SALTIM,NAVALUE)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [str(i)] + row)
            i += 1

    # Commit the changes to the database

    conn.commit()
    cursor.close()
    conn.close()


