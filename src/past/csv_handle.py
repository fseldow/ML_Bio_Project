import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from closest_index import buildDict
import csv_utils as utils

# main
df = pd.read_csv('E:/python/Tadpole/Full_List_sorted.csv')
sim_dic=buildDict(df)#dict ptid:similar ptid
ptid_split=utils.build_ptid_split_dic(df) #dict ptid:[start_row,end_row]
df=utils.timeFormat(df)

dataIndex=[]#data column need compensation
for (index_name,type) in df.dtypes.items():
    if type=='float64' and index_name!='DXCHANGE':
        dataIndex.append(index_name)

for item in dataIndex:
    print('handle '+item)
    for (id,thing) in ptid_split.items():
        df = utils.compenWithDict(df,item,sim_dic,ptid_split,id,[])
    df = utils.dataCompen(df, item)

df.to_csv('E:/python/Tadpole/test.csv', index=False)