import pandas as pd
import conf as conf
import src.preprocess.csv_utils as utils
import os



def auto_compen():
    df = pd.read_csv(conf.raw_dir+'TADPOLE_InputData.csv')
    print('start auto_patient compenation')
    #drop col or row with too many NaN
    percent_row=0.3
    percent_col=0.3
    df=df.dropna(0,subset=['PTID_Key','EXAMDATE'])
    #df=df.dropna(axis=0,thresh=int(df.shape[1]*percent_row))
    df=df.dropna(axis=1,thresh=int(df.shape[0]*percent_col))
    print('shape after first drop',df.shape)

    basicIndex=['PTID','AGE','PTGENDER','PTGENDER','PTEDUCAT','PTETHCAT','PTMARRY',]
    dataIndex=[]

    df=utils.timeFormat(df)
    # sort
    order=['PTID_Key','EXAMDATE']
    df = df.sort_values(by=order)
    df.index = pd.RangeIndex(len(df.index))
    df.to_csv('sorted_input.csv',index=False)

    df=utils.handleDX(df)

    for (index_name,type) in df.dtypes.items():
        if type=='float64' and index_name!='DXCHANGE':
            dataIndex.append(index_name)
        if '_bl' in index_name:
            basicIndex.append(index_name)

    print('compenate float data')
    for item in dataIndex:
        df=utils.dataCompen(df,item)

    print('auto_patient compenation completed.')
    df.to_csv('Full_List_sorted.csv', index=False)
    try:
        df.to_csv(conf.intermediate_dir+'auto_com.csv', index=False)
    except:
        print('write auto_com.csv fail')


    return df

##############################################################################
def cor_compen(df,flag=False):
    if flag:
        df = pd.read_csv(conf.intermediate_dir+'auto_com.csv')
    print('start cor-patient comenation')
    sim_dic=utils.buildDict(df)#dict ptid:similar ptid

    ptid_split=utils.build_ptid_split_dic(df) #dict ptid:[start_row,end_row]
    df=utils.timeFormat(df)

    dataIndex=[]#data column need compensation
    for (index_name,type) in df.dtypes.items():
        if type=='float64' and index_name!='DXCHANGE':
            dataIndex.append(index_name)

    for item in dataIndex:
        for (id,thing) in ptid_split.items():
            df = utils.compenWithDict(df,item,sim_dic,ptid_split,id,[])
        df = utils.dataCompen(df, item)
    print('cor-patient completed')
    try:
        df.to_csv(conf.intermediate_dir+'cor_com.csv', index=False)
    except:
        print('write cor_com.csv fail')
    return df

################################################################################
def final_drop(df,flag=False):
    print('start final drop')
    if flag:
        df = pd.read_csv(conf.intermediate_dir+'cor_com.csv')

    df = df.dropna(axis=1, thresh=int(df.shape[0] * 0.8))
    df.index = pd.RangeIndex(len(df.index))
    df = utils.finalAdd(df)

    drop_list = ['DX', 'Month', 'M', 'Years_bl', 'Month_bl']
    for (index_name, type) in df.dtypes.items():
        if 'DATE' in index_name:
            drop_list.append(index_name)
    df = df.drop(axis=1, labels=drop_list)

    try:
        df.to_csv(conf.intermediate_dir+'final_drop.csv', index=False)
    except:
        print('write final_drop.csv fail')
    return df
##################################################################################
def normalization(df,flag=False):
    print('normalization')
    if flag:
        df = pd.read_csv(conf.intermediate_dir + 'final_drop.csv')

    for (index_name,type) in df.dtypes.items():
        if type!='float64':
            df=utils.char2float(df,index_name)
            df=df.drop(axis=1,labels=index_name)


    normal_list=[]
    for (index_name,type) in df.dtypes.items():
        if index_name not in ['DXCHANGE','ADAS13','Ventricles','MMSE']:
            normal_list.append(index_name)
    utils.normalization(df,normal_list)

    df['Ventricles_Norm']=df['Ventricles']

    try:
        df.to_csv(conf.intermediate_dir+'norm.csv', index=False)
    except:
        print('write norm.csv fail')
    return df

##################################################################################

