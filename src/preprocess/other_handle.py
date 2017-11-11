import pandas as pd
import src.preprocess.csv_utils as utils
import conf as conf

y_index=['DXCHANGE','ADAS13','Ventricles_Norm','MMSE']
x_index=['AGE','PTGENDER','PTEDUCAT','PTETHCAT','PTRACCAT','PTMARRY','APOE4']

def sort_train(df):
    df['Date'] = pd.to_datetime(df['Date'])
    order = ['PTID_Key', 'Date']
    df = df.sort_values(by=order)
    df.index = pd.RangeIndex(len(df.index))
    df['DXCHANGE'] = df['CN_Diag'] + 2 * df['MCI_Diag'] + 3 * df['AD_Diag']
    df = df.drop(['CN_Diag', 'MCI_Diag', 'AD_Diag'], axis=1)
    return df

def mergeFiles(input_df,target_df):
    input_dict=utils.build_ptid_split_dic(input_df)
    target_dict=utils.build_ptid_split_dic(target_df)
    list = []
    for (item, type) in input_df.dtypes.items():
        if item not in y_index and item!='PTID_Key':
            list.append(item)
            target_df[item]=None
    #persist train
    for i in range(len(target_df.index)):
        print(i,'in',len(target_df.index))
        id=target_df['PTID_Key'][i]
        start_in_train=target_dict[id][0]
        end_in_train = target_dict[id][1]
        start_in_input=input_dict[id][0]
        end_in_input=input_dict[id][1]
        #if end_in_input==start_in_input:
            #delta_month=1
        #else:
            #delta_month = input_df['M'][end_in_input] - input_df['M'][end_in_input-1]
        if i==start_in_train:
            end_in_input=end_in_input
            target_df.loc[i,list]=input_df.loc[end_in_input,list]
        else:
            target_df.loc[i, list] = target_df.loc[i-1, list]
        #target_df.loc[i,'M']=delta_month*(i-start_in_train+1)+input_df['M'][end_in_input]


    return target_df

def input2train(input_df,input_dict=[]):
    input_dict = utils.build_ptid_split_dic(input_df)
    list=[]
    for (item, type) in input_df.dtypes.items():
        if item not in y_index+x_index+['PTID_Key','M']:
            list.append(item)

    for (id,range) in input_dict.items():
        print(id,'in',len(input_dict))
        input_df.loc[range[0]:range[1],list]=input_df.loc[range[0]:range[1],list].shift(1)
    input_df=input_df.dropna(axis=0,how='any')
    return input_df

def add_last_y2h(input_df):
    add_index=['DXCHANGE','MMSE','ADAS13','Ventricles_Norm']
    add_to=['DXCHANGE_PRE','MMSE_PRE','ADAS13_PRE','Ventricles_Norm_PRE']
    input_df[add_to]=input_df[add_index]
    return input_df




def shift_datas(input_flag=True,train_flag=True,test_flag=True,validation_flag=True):
    print('start shift')
    input_df = pd.read_csv(conf.intermediate_dir+'norm.csv')
    input_df = add_last_y2h(input_df)
    if train_flag:
        train_df = pd.read_csv(conf.raw_dir+'TADPOLE_TargetData_train.csv')
        train_df = sort_train(train_df)
        train_df = train_df.drop('Date', 1)
        # train_df.to_csv('train_sorted.csv', index=False)
        train_df = mergeFiles(input_df, train_df)
        train_df.to_csv(conf.result_dir+'train_add.csv', index=False)

    if test_flag:
        test_df = pd.read_csv(conf.raw_dir+'TADPOLE_TargetData_test.csv')
        test_df = sort_train(test_df)
        test_df = test_df.drop('Date', 1)
        # test_df.to_csv('test_sorted.csv', index=False)
        test_df = mergeFiles(input_df, test_df)
        test_df.to_csv(conf.result_dir+'test_add.csv', index=False)

    if validation_flag:
        val_df = pd.read_csv(conf.raw_dir+'TADPOLE_PredictTargetData_valid.csv')
        val_df = sort_train(val_df)
        # val_df=val_df.drop('Date',1)
        val_df.to_csv(conf.result_dir+'val_sorted.csv', index=False)
        val_df = mergeFiles(input_df, val_df)
        val_df.to_csv(conf.result_dir+'val_add.csv', index=False)

    if input_flag:
        input_df=input2train(input_df)
        input_df.to_csv(conf.result_dir+'input_shift.csv', index=False)