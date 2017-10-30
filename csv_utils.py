import pandas as pd
import numpy as np
import re

def getDX_change(dx):
    return{
        'NL':1,
        'MCI':2,
        'Dementia':3
    }[dx]

#handle leaky DX column
def handleDX(df):
    dx=df['DX']
    ptid=df['PTID_Key']
    dx_change=df['DXCHANGE']
    last_valid=0
    next_valid=len(dx)-1
    current_pt=ptid[0]
    for i in range(len(dx)):
        #print(i,ptid[i])
        if ptid[i]!=current_pt:
            last_valid=i
            current_pt=ptid[i]
        if pd.isnull(dx[i]):
            # search backward
            next_valid = len(dx)-1
            for j in range(i+1,len(dx)):
                if ptid[j]!=current_pt:
                    next_valid=j-1
                    break
                if pd.notnull(dx[j]):
                    next_valid=j
                    break
            if dx[last_valid]==dx[next_valid]:
                for j in range(last_valid+1,next_valid):
                    df.set_value(j,'DX',dx[last_valid])
                    df.set_value(j,'DXCHANGE',dx_change[last_valid])
                    #dx[j]=dx[last_valid]
                    #dx_change[j]=dx_change[last_valid]
            else:
                p=re.compile(' to ')
                if pd.notnull(dx[last_valid]):
                    f=p.split(dx[last_valid])
                    if(len(f)==2):
                        value=getDX_change(f[1])
                        for j in range(last_valid,next_valid):
                            df.set_value(j, 'DX', f[1])
                            df.set_value(j, 'DXCHANGE', value)
                            #dx[j]=f[1]
                            #dx_change[j]=value
                if pd.notnull(dx[next_valid]):
                    b=p.split(dx[next_valid])
                    if(len(b)==2):
                        value=getDX_change(b[0])
                        for j in range(next_valid-1,last_valid,-1):
                            df.set_value(j, 'DX', b[0])
                            df.set_value(j, 'DXCHANGE', value)
            last_valid=next_valid
            i=last_valid
        else:
            last_valid=i
    return df

#linear handle leaky data
def dataCompen(df,index):
    list=df[index]
    time=df['M']
    ptid=df['PTID_Key']
    last_valid = 0
    next_valid = len(list) - 1
    current_pt = ptid[0]
    for i in range(len(list)):
        #print(i,ptid[i])
        if ptid[i]!=current_pt:
            last_valid=i
            current_pt=ptid[i]
        if pd.isnull(list[i]):
            # search backward
            next_valid = len(list)-1
            for j in range(i+1,len(list)):
                if ptid[j]!=current_pt:
                    next_valid=j-1
                    break
                if pd.notnull(list[j]):
                    next_valid=j
                    break
            if pd.notnull(list[last_valid]) and pd.notnull(list[next_valid]):
                slope=(list[next_valid]-list[last_valid])/(time[next_valid]-time[last_valid])
                for j in range(last_valid+1,next_valid):
                    value=slope*(time[j]-time[last_valid])+list[last_valid]
                    df.set_value(j,index,value)
            last_valid = next_valid
            i=last_valid
        else:
            last_valid=i
    return df

# build dict to link ptid to row in input.csv
# dict ptid:[start_row,end_row]
def build_ptid_split_dic(df):
    ptid_f=df['PTID_Key']
    dict={}
    current_pt=ptid_f[0]
    start=0
    for i in range(len(ptid_f.index)):
        if current_pt!=ptid_f[i]:
            dict[current_pt]=[start,i-1]
            current_pt=ptid_f[i]
            start=i
    dict[current_pt]=[start,len(ptid_f.index)-1]
    return dict

# use similar patient to handle leaky data
def compenWithDict(df,index,sim_dict,ptid_split,ptid,last_id=[]):
    start_row=ptid_split[ptid][0]
    end_row=ptid_split[ptid][1]
    if pd.notnull(df[index][start_row]):
        return df
    if ptid not in sim_dict.keys():
        return df
    nextPt=sim_dict[ptid]
    if(nextPt in last_id):
        return df
    last_id.append(ptid)
    df=compenWithDict(df,index,sim_dict,ptid_split,nextPt,last_id)

    next_start_row = ptid_split[nextPt][0]
    next_end_row = ptid_split[nextPt][1]

    # next is also empty
    if pd.isnull(df[index][next_start_row]):
        return df
    # next have value
    df.set_value(start_row,index,df[index][next_start_row])

    j=next_start_row
    for i in range(start_row+1,end_row+1):
        month=df['Month'][i]
        if j>next_end_row:
            break
        for j in range(next_start_row,next_end_row+1):
            month_next=df['Month'][j]
            if month==month_next:
                df.set_value(i,index,df[index][j])
                break
            if month<month_next:
                month_next_pre=df['Month'][j-1]
                value=(df[index][j]-df[index][j-1])/(month_next-month_next_pre)*(month-month_next_pre)+df[index][j-1]
                df.set_value(i,index,value)
                break
    return df

#change date
def timeFormat(df):
    dateIndex=['EXAMDATE',
               'EXAMDATE_bl',
               'EXAMDATE_UCSFFSL_02_01_16_UCSFFSL51ALL_08_01_16',
               'VERSION_UCSFFSL_02_01_16_UCSFFSL51ALL_08_01_16',
               'EXAMDATE_UCSFFSX_11_02_15_UCSFFSX51_08_01_16',
               'VERSION_UCSFFSX_11_02_15_UCSFFSX51_08_01_16',
               'RUNDATE_BAIPETNMRC_09_12_16',
               'EXAMDATE_UCBERKELEYAV1451_10_17_16',
               'EXAMDATE_DTIROI_04_30_14',
               'EXAMDATE_UPENNBIOMK9_04_19_17',
               'RUNDATE_UPENNBIOMK9_04_19_17']
    for col in dateIndex:
        try:
            df[col]=pd.to_datetime(df[col])
        except:
            print(col+' removed')
    return df

'''
# main
df = pd.read_csv('E:/python/public/TADPOLE_InputData.csv')

#drop col or row with too many NaN
percent_row=0.3
percent_col=0.3
df=df.dropna(0,subset=['PTID_Key','EXAMDATE'])
print(df.shape)
#df=df.dropna(axis=0,thresh=int(df.shape[1]*percent_row))
df=df.dropna(axis=1,thresh=int(df.shape[0]*percent_col))
print(df.shape)




basicIndex=['PTID','AGE','PTGENDER','PTGENDER','PTEDUCAT','PTETHCAT','PTMARRY',]
dataIndex=[]



order=['PTID_Key','EXAMDATE']
df = df.sort_values(by=order)
df.index = pd.RangeIndex(len(df.index))


df=handleDX(df)

for (index_name,type) in df.dtypes.items():
    if type=='float64' and index_name!='DXCHANGE':
        dataIndex.append(index_name)
    if '_bl' in index_name:
        basicIndex.append(index_name)


for item in dataIndex:
    print('handle '+item)
    df=dataCompen(df,item)

df.to_csv('Full_List_sorted.csv', index=False)
'''
