import pandas as pd
import csv_utils as utils
#import keras

y_index=['DXCHANGE','Ventricles','ADAS13','Ventricles_Norm','MMSE']
x_index=['AGE','PTGENDER','PTEDUCAT','PTETHCAT','PTRACCAT','PTMARRY','APOE4']

def sort_train(df):
    df['Date'] = pd.to_datetime(df['Date'])
    order = ['PTID_Key', 'Date']
    df = df.sort_values(by=order)
    df.index = pd.RangeIndex(len(df.index))
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
        if end_in_input==start_in_input:
            delta_month=1
        else:
            delta_month = input_df['M'][end_in_input] - input_df['M'][end_in_input-1]
        if i==start_in_train:
            end_in_input=end_in_input
            target_df.loc[i,list]=input_df.loc[end_in_input,list]
        else:
            target_df.loc[i, list] = target_df.loc[i-1, list]
        target_df.loc[i,'M']=delta_month*(i-start_in_train+1)+input_df['M'][end_in_input]


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
    input_df.dropna(inplace=True)
    return input_df




train_df = pd.read_csv('../public/TADPOLE_TargetData_train.csv')
train_df=sort_train(train_df)

train_df=train_df.drop('Date',1)
print(train_df.values)
train_df.to_csv('train_sorted.csv', index=False)

test_df = pd.read_csv('../public/TADPOLE_TargetData_test.csv')
test_df = sort_train(test_df)
test_df=test_df.drop('Date',1)
#test_df.to_csv('test_sorted.csv', index=False)

input_df = pd.read_csv('after_drop.csv')
#test_df=mergeFiles(input_df,test_df)

input_df=input2train(input_df)
input_df.to_csv('input_shift.csv', index=False)





