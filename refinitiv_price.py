import os
from datetime import datetime, timedelta
import pandas as pd
import refinitiv.data as rd


def populate(uuid, ric):
    pd.set_option('display.max_columns', None)
    os.environ["RD_LIB_CONFIG_PATH"] = "./Configuration"
    rd.open_session()

    today = datetime.now().date()
    attempts = 0

    flds = ["TRDPRC_1", "HIGH_1", "LOW_1", "ACVOL_UNS", "OPEN_PRC", "BID", "ASK"]

    while attempts < 30:
        yesterday = today - timedelta(days=1)
        print("Today's date:", today.strftime('%Y-%m-%d'))
        print("Yesterday's date:", yesterday.strftime('%Y-%m-%d'))
        try:
            a = rd.get_history(universe=ric, fields=flds, interval='tas', count=1)
            if a.isnull().values.any():
                a = rd.get_history(universe=ric, fields=flds, start=yesterday, end=today, count=1)
            else:
                pass
        except:
            a = rd.get_history(universe=ric, fields=flds, start=yesterday, end=today, count=1)
        b = pd.DataFrame(a)
        if len(b) != 0:
            b.to_csv(f'./Output/{uuid}-refinitiv.csv', index=True)
            break
        else:
            today = today - timedelta(days=1)

    rd.close_session()

