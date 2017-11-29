import pandas as pd
import numpy as np
import conf
y_index=['DXCHANGE','ADAS13','Ventricles_Norm','MMSE']
x_index_helper=['AGE','PTGENDER','PTEDUCAT','PTETHCAT','PTRACCAT','PTMARRY','APOE4','DX_bl']
x_index=[]
h_index = []
input_df = pd.read_csv(conf.intermediate_dir+'norm.csv')
for (item, type) in input_df.dtypes.items():
    for i in x_index_helper:
        if i in item:
            x_index.append(item)
            break
for (item, type) in input_df.dtypes.items():
    if item not in x_index+y_index+['PTID_Key','M'] and '_bl' not in item:
        h_index.append(item)
