import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from closest_index import buildDict
import test_pd as test

# main
df = pd.read_csv('E:/python/Tadpole/Full_List_sorted.csv')
sim_dic=buildDict(df)#dict ptid:similar ptid
ptid_split=test.build_ptid_split_dic(df) #dict ptid:[start_row,end_row]

dataIndex=['LONISID_UCSFFSL_02_01_16_UCSFFSL51ALL_08_01_16']#data column need compensation #test BK
'''
for (index_name,type) in df.dtypes.items():
    if type=='float64' and index_name!='DXCHANGE':
        dataIndex.append(index_name)
'''
for item in dataIndex:
    print('handle '+item)
    for (id,thing) in ptid_split.items():
        df=test.compenWithDict(df,item,sim_dic,ptid_split,id)

df.to_csv('E:/python/Tadpole/test.csv', index=False)