import pandas as pd
import cmath as math

def evaluateClassification(real,result):
    dict_real_poss= {
        1:0,
        2:0,
        3:0
    }
    dict_result_poss = {
        1:0,
        2:0,
        3:0
    }
    n1=0
    n2=0
    sim=0
    for i in range(len(real.index)):
        if pd.notnull(real['DXCHANGE'][i]):
            dict_real_poss[real['DXCHANGE'][i]] += 1
            if real['DXCHANGE'][i]==result['DXCHANGE'][i]:
                sim+=1
            n1+=1
        if result['DXCHANGE'][i]<=3:
            dict_result_poss[result['DXCHANGE'][i]] += 1
            n2+=1
    loss=0
    for i in range(1,4):
        loss+=-dict_real_poss[i]/n1*math.log(dict_result_poss[i]/n2)
    loss/=3
    print(loss,sim/n1)
    return loss
def evaluateRegression(real,result):
    list=['ADAS13','MMSE','Ventricles_Norm']
    ret=[]
    for item in list:
        loss=0
        n=0
        for i in range(len(real)):
            if pd.notnull(real[item][i]):
                loss+=(real[item][i]-result[item][i])**2
                n+=1
        if n!=0:
            loss/=n
        ret.append((item,loss))
    print('MSD',ret)
    return ret
def evaluateMAD(real,result):
    list=['ADAS13','MMSE','Ventricles_Norm']
    ret=[]
    for item in list:
        loss=0
        n=0
        for i in range(len(real)):
            if pd.notnull(real[item][i]):
                loss+=abs(real[item][i]-result[item][i])
                n+=1
        if n!=0:
            loss/=n
        ret.append((item,loss))
    print('MAD',ret)
    return ret

train_real = pd.read_csv('train_sorted.csv')
test_real = pd.read_csv('test_sorted.csv')
train_result=pd.read_csv('result_train.csv')
test_result=pd.read_csv('result_test.csv')

dx_train_data_real=train_real['DXCHANGE'].values
dx_train_data_result=train_result['DXCHANGE'].values
dx_test_data_real=test_real['DXCHANGE'].values
dx_test_data_result=test_result['DXCHANGE'].values

other_train_data_real=train_real.drop(['DXCHANGE','PTID_Key'],axis=1)
other_train_data_result=train_result.drop(['DXCHANGE','PTID_Key'],axis=1)
other_test_data_real=test_real.drop(['DXCHANGE','PTID_Key'],axis=1)
other_test_data_result=test_result.drop(['DXCHANGE','PTID_Key'],axis=1)

evaluateRegression(train_real,train_result)
evaluateRegression(test_real,test_result)

evaluateMAD(train_real,train_result)
evaluateMAD(test_real,test_result)

evaluateClassification(train_real,train_result)
evaluateClassification(test_real,test_result)