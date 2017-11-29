import pandas as pd
import src.preprocess.csv_utils as utils
import conf


# solve for a and b
def best_fit(X, Y):
    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)
    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2
    b = numer / denum
    a = ybar - b * xbar
    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))
    return a, b

def sort_train(df):
    df['Date'] = pd.to_datetime(df['Date'])
    order = ['PTID_Key', 'Date']
    df = df.sort_values(by=order)
    df.index = pd.RangeIndex(len(df.index))
    df['DXCHANGE']=df['CN_Diag']+2*df['MCI_Diag']+3*df['AD_Diag']
    df=df.drop(['CN_Diag','MCI_Diag','AD_Diag'],axis=1)
    return df

def baselineAlgorithm(input_df,target_df):
    input_dict = utils.build_ptid_split_dic(input_df)
    target_dict = utils.build_ptid_split_dic(target_df)
    classification_list = ['DXCHANGE']
    regression_list=['ADAS13','Ventricles_Norm','MMSE']
    # persist train
    for item in regression_list:
        for i in range(len(target_df.index)):
            print(i, 'in', len(target_df.index))
            id = target_df['PTID_Key'][i]
            start_in_train = target_dict[id][0]
            end_in_train = target_dict[id][1]
            start_in_input = input_dict[id][0]
            end_in_input = input_dict[id][1]
            if end_in_input == start_in_input:
                delta_month = 0
            else:
                delta_month = input_df[item][end_in_input] - input_df[item][end_in_input - 1]
            if i == start_in_train:
                end_in_input = end_in_input
                target_df.loc[i, classification_list] = input_df.loc[end_in_input, classification_list]
            else:
                target_df.loc[i, classification_list] = target_df.loc[i - 1, classification_list]
            target_df.loc[i, item] = delta_month * (i - start_in_train + 1) + input_df[item][end_in_input]
    return target_df

train_df = pd.read_csv(conf.raw_dir+'TADPOLE_TargetData_train.csv')
train_df=sort_train(train_df)
train_df=train_df.drop('Date',1)
#train_df.to_csv('train_sorted.csv', index=False)

test_df = pd.read_csv(conf.raw_dir+'TADPOLE_TargetData_test.csv')
test_df = sort_train(test_df)
test_df=test_df.drop('Date',1)
#test_df.to_csv('test_sorted.csv', index=False)

val_df = pd.read_csv(conf.raw_dir+'TADPOLE_TargetData_valid.csv')
val_df = sort_train(val_df)
val_df=val_df.drop('Date',1)

input_df = pd.read_csv(conf.intermediate_dir+'norm.csv')
result_train=baselineAlgorithm(input_df,train_df)
result_train.to_csv(conf.result_dir+'result_train.csv', index=False)
result_test=baselineAlgorithm(input_df,test_df)
result_test.to_csv(conf.result_dir+'result_test.csv', index=False)
result_val=baselineAlgorithm(input_df,val_df)
result_val.to_csv(conf.result_dir+'result_validation.csv', index=False)