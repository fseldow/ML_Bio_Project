import pandas as pd
import numpy as np
y_index=['DXCHANGE','ADAS13','Ventricles_Norm','MMSE']
x_index=['AGE','PTGENDER','PTEDUCAT','PTETHCAT','PTRACCAT','PTMARRY','APOE4','DX_bl']
h_index = []
input_df = pd.read_csv('input_shift.csv')
for (item, type) in input_df.dtypes.items():
    if item not in x_index+y_index+['PTID_Key','M'] and '_bl' not in item:
        h_index.append(item)
