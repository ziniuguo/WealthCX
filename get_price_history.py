import os
import refinitiv.data as rd
import pandas as pd
import get_RIC
pd.set_option('display.max_columns', None)
os.environ["RD_LIB_CONFIG_PATH"] = "./Configuration"
rd.open_session()

columns = get_RIC.get_ric()
print('columns:'+columns[0])
a = rd.get_history(universe=columns[0:10],start='2023-10-29',end='2023-10-31')
b = pd.DataFrame(a)
print(b)
b.to_csv('output.csv', index=True)  # index=False 用于不保存行索引

rd.close_session()