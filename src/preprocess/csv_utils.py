import pandas as pd
import numpy as np
import re

def getDX_change(dx):
    return{
        'NL':1,
        'MCI':2,
        'Dementia':3
    }[dx]

def DXbl2DX(dx_bl):
    if 'CI' in dx_bl:
        return 'MCI'
    if dx_bl=='CN':
        return 'NL'
    return 'Dementia'

#handle leaky DX column
def handleDX(df):
    print('compenating dx')
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
                    b = p.split(dx[next_valid])
                    if (len(b) == 2):
                        value = getDX_change(b[0])
                        for j in range(next_valid - 1, last_valid, -1):
                            df.set_value(j, 'DX', b[0])
                            df.set_value(j, 'DXCHANGE', value)
                if pd.isnull(dx[next_valid]) and pd.notnull(dx[last_valid]):
                    value = dx[last_valid]
                    for j in range(next_valid,last_valid,-1):
                        df.set_value(j, 'DX', value)
                        df.set_value(j, 'DXCHANGE', getDX_change(value))
                if pd.isnull(dx[last_valid]) and pd.isnull(dx[next_valid]):
                    value=DXbl2DX(df['DX_bl'][last_valid])
                    for j in range(last_valid,next_valid+1):
                        df.set_value(j,'DX',value)
                        df.set_value(j, 'DXCHANGE', getDX_change(value))
            last_valid=next_valid
            i=last_valid
        else:
            last_valid=i
    return df

#linear handle leaky data
def dataCompen(df,index):
    print('float data handling ' ,index)
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

def normalization(bf,data_df):
    for item in data_df:
        if item=='PTID_Key':
            continue
        try:
            max=bf[item].max(axis=0)
            min=bf[item].min(axis=0)
            bf[item]=(bf[item]-min)/(max-min)
        except:
            print(item+' constant')
    return bf

def calculateDiff(norm_bf,data_df,i,j):
    sum=0
    for item in data_df:
        if item=='PTID_Key':
            continue
        sum+=(norm_bf[item][i]-norm_bf[item][j])**2
    sum/=len(data_df)
    return sum

def pairClosest(bf,string_df,dict,level=1):
    data_df=[]
    #string_df=[]
    #dict={}
    for (index_name,type) in bf.dtypes.items():
        if type=='float64':
            data_df.append(index_name)
        #else:
            #if 'DATE'not in index_name:
                #string_df.append(index_name)
    bf=bf.sort_values(by=string_df)
    bf.index = pd.RangeIndex(len(bf.index))

    #print(bf.head())
    #print('len',len(bf.index))
    #bf.to_csv('E:/bf_test.csv', index=False)
    start_id=0
    end_id=len(bf.index)

    try:
        last_string_index=string_df[len(string_df)-level]
    except:
        print('level should be 1~len(string_df)')
        return -1
    record=bf[last_string_index][0]

    norm_bf=normalization(bf,data_df)
    for i in range(0,len(bf.index)):
        #print(i)
        if bf[string_df[0]][i]!=record:
            record=bf[last_string_index][i]
            start_id=i
            end_id=len(bf.index)
        Min=[-1,-1]
        if bf['PTID_Key'][i] in dict.keys():
            continue
        for j in range(start_id,min(len(bf.index),end_id)):
            if bf[last_string_index][j]!=record:
                end_id=j
                break
            if j==i:
                continue
            dif=calculateDiff(norm_bf,data_df,i,j)
            if Min[1]==-1 or Min[1]>dif:
                Min=[j,dif]
        if Min[0]>=0:
            dict[bf['PTID_Key'][i]]=bf['PTID_Key'][Min[0]]
    return dict

# build similar dictionary
def buildDict(df):
    print('start building similar dictionary')
    basicIndex=['PTID_Key','AGE','PTGENDER','PTEDUCAT','PTETHCAT','PTMARRY','APOE4']
    for (index_name,type) in df.dtypes.items():
        if '_bl' in index_name and 'Years' not in index_name and 'Month' not in index_name:
            basicIndex.append(index_name)
    df=df.dropna(0,subset=['PTID_Key','EXAMDATE'])
    bf=df[basicIndex]
    bf=bf.dropna(1)
    bf=bf.drop_duplicates()
    level=1
    dict={}
    string_df=['DX_bl','PTGENDER','PTETHCAT']
    while len(dict)<len(bf.index) and level<=len(string_df):
        dict=pairClosest(bf,string_df,dict,level)
        level+=1
        print('dict size',len(dict),'total',len(bf.index))
    return dict


def finalAdd(df):
    for (index,type) in df.dtypes.items():
        print('final handle',index)
        for i in range(len(df.index)):
            if pd.isnull(df[index][i]):
                if i>0 and type=='float64':
                    if df['PTID_Key'][i]==df['PTID_Key'][i-1]:
                        if df['Month'][i-1]==0:
                            df.set_value(i,index,df[index][i-1])
                        else:
                            value=2*df[index][i - 1]-df[index][i-2]
                            df.set_value(i, index, value)
                else:
                    if i>0:
                        if df['PTID_Key'][i] == df['PTID_Key'][i - 1]:
                            df.set_value(i, index, df[index][i - 1])
    return df

def char2float(df,index):
    print('change type',index)
    results=[]
    for i in range(len(df.index)):
        if df[index][i] not in results:
            results.append(df[index][i])
    for item in results:
        new_index=index+'_'+item
        df[new_index]=pd.Series(0,index=df.index)
    for i in range(len(df.index)):
        target=index+'_'+df[index][i]
        df.set_value(i,target,1)
    return df
