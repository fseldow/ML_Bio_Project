import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def leakyUnit(df,first_index,second_index):
    for i in range(len(df.index)):
        try:
            for item in first_index:
                a=1
        except:
            a=1
    return df
def finalAdd(df):
    for (index,type) in df.dtypes.items():
        print('handle',index)
        for i in range(len(df.index)):
            if pd.isnull(df[index][i]):
                if i>0 and type=='float64':
                    if df['PTID_Key'][i]==df['PTID_Key'][i-1]:
                        if df['Month'][i-1]==0:
                            df.set_value(i,index,df[index][i-1])
                        else:
                            value=2*df[index][i - 1]-df[index][i-2]
                            df.set_value(i, index, df[index][i - 1])
                else:
                    if i>0:
                        if df['PTID_Key'][i] == df['PTID_Key'][i - 1]:
                            df.set_value(i, index, df[index][i - 1])

    return df

df = pd.read_csv('test.csv')
df=df.dropna(axis=1,thresh=int(df.shape[0]*0.8))
df.index = pd.RangeIndex(len(df.index))
df=finalAdd(df)
df.to_csv('after_drop.csv', index=False)