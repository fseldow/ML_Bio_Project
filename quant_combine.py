import os
import pandas as pd
import numpy as np
#-----------------------------------------------------------------
#read from dropout to out.csv(quantify all non numeric attributes)
# ad=pd.read_csv('after_drop.csv')
# print(ad.loc[:])
# for item in ['Years_bl','Month_bl','Month','M','DX','EXAMDATE_bl','EXAMDATE']:
#     ad=ad.drop(item,1)
# classes=['CN','LMCI','EMCI','AD','SMC','Male','Female','Unknown','Not Hisp/Latino','Hisp/Latino','Hawaiian/Other PI','Am Indian/Alaskan','White','Black','Asian','More than one','Never married','Married','Divorced','Widowed']
# labels=[0,1,2,3,4,0,1,2,0,1,2,3,0,1,2,3,4,0,1,2,3]
'''
for i in range(len(ad.iloc[:,1])):
    if ad.loc[i,'DX_bl']=='EMCI':
        ad.loc[i,'DX_bl']=1
    if ad.loc[i,'DX_bl']=='AD':
        ad.loc[i,'DX_bl']=2
    if ad.loc[i,'DX_bl']=='CN':
        ad.loc[i,'DX_bl']=3
    if ad.loc[i,'DX_bl']=='LMCI':
        ad.loc[i,'DX_bl']=4
    if ad.loc[i,'DX_bl']=='SMC':
        ad.loc[i,'DX_bl']=5
    if ad.loc[i,'PTGENDER']=='Male':
        ad.loc[i,'PTGENDER']=0
    if ad.loc[i,'PTGENDER']=='Female':
        ad.loc[i,'PTGENDER']=1
    if ad.loc[i,'PTETHCAT']=='Not Hisp/Latino':
        ad.loc[i,'PTETHCAT']=0
    if ad.loc[i,'PTETHCAT']=='Hisp/Latino':
        ad.loc[i,'PTETHCAT']=1
    if ad.loc[i,'PTRACCAT']=='White':
        ad.loc[i,'PTRACCAT']=1
    if ad.loc[i,'PTRACCAT']=='Black':
        ad.loc[i,'PTRACCAT']=2
    if ad.loc[i,'PTRACCAT']=='More than one':
        ad.loc[i,'PTRACCAT']=3
    if ad.loc[i, 'PTRACCAT'] == 'Asian':
        ad.loc[i, 'PTRACCAT'] = 4
    if ad.loc[i,'PTMARRY']=='Married':
        ad.loc[i,'PTMARRY']=1
    elif ad.loc[i, 'PTMARRY'] == 'Divorced':
        ad.loc[i, 'PTMARRY'] = 2
    elif ad.loc[i,'PTMARRY']=='Widowed':
        ad.loc[i,'PTMARRY']=3
    else:
        ad.loc[i,'PTMARRY']=4'''
# for i in range(len(ad.iloc[:,1])):
#     for j in range(len(ad.iloc[1,:])):
#         if ad.iloc[i,j] not in classes:
#             continue
#         class_id=classes.index(ad.iloc[i,j])
#         ad.iloc[i,j]=labels[class_id]
#-----------------------------------------------------------------
seg=pd.read_csv('out.csv')
new=seg
new.loc[:,0]=seg.iloc[:,0]
new.iloc[:,1:6]=seg.loc[:,'AGE':'PTMARRY']


seg.to_csv('input_final.csv',index=False)
