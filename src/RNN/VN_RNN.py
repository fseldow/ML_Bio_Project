import pandas as pd
import src.RNN.X_Y_H as ref
from keras.models import  Model,optimizers
from keras.layers import Dense, Input,Dropout
from keras.models import Sequential
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
import src.preprocess.csv_utils as utils
import numpy as np
from src.evaluate import evaluateRegression
import conf
Target='Ventricles_Norm'


loss_train=[]
loss_test=[]
loss_validation=[]
loss_true_train=[]


def predict_state(Encoder,Model,target_df):
    target_dict = utils.build_ptid_split_dic(target_df)
    for i in range(len(target_df.index)):
        #print(i, 'in', len(target_df.index))
        id = target_df['PTID_Key'][i]
        start_in_train = target_dict[id][0]
        end_in_train = target_dict[id][1]
        if i!=start_in_train:
            X_test=target_df.loc[i-1,ref.h_index+ref.x_index].as_matrix(columns=None)
            temp=Encoder.predict(np.expand_dims(X_test, axis=0))
            for j in range(len(ref.h_index)):
                target_df.set_value(i,ref.h_index[j],temp[0,j])
    return target_df

def predict_result(Encoder,Model,target_df):
    target_dict = utils.build_ptid_split_dic(target_df)
    for i in range(len(target_df.index)):
        #print(i, 'in', len(target_df.index))
        id = target_df['PTID_Key'][i]
        start_in_train = target_dict[id][0]
        end_in_train = target_dict[id][1]
        if i != start_in_train:
            X_test = target_df.loc[i - 1, ref.h_index + ref.x_index].as_matrix(columns=None)
            temp = Encoder.predict(np.expand_dims(X_test, axis=0))
            for j in range(len(ref.h_index)):
                target_df.set_value(i, ref.h_index[j], temp[0, j])
        X_test_t = target_df.loc[i, ref.h_index + ref.x_index].as_matrix(columns=None)
        result=Model.predict(np.expand_dims(X_test_t, axis=0))
        target_df.set_value(i,Target,result)
    return target_df

def getTrain(input_df,train_df):
    #train_df=pd.concat((input_df,train_df))
    #train=train.sort_values(by=['PTID_Key','M'])
    #train.index = pd.RangeIndex(len(train.index))
    #train=utils.dataCompen(train,Target)
    train = train_df.dropna(axis=0, subset=[Target])
    return train

epochs=10

input_shift=pd.read_csv(conf.intermediate_dir+'input_shift.csv')
train_add=pd.read_csv(conf.intermediate_dir+'train_add.csv')
train=getTrain(input_shift,train_add)
train=input_shift


X_train=train[ref.h_index+ref.x_index].values
Y_train=train[Target].values


input=Input(shape=(X_train.shape[1],))
hidden1=Dense(100, activation='relu')(input)
hidden1_1=Dense(100, activation='relu')(hidden1)
hidden2=Dense(len(ref.h_index),activation='relu')(hidden1_1)
hidden2_1=Dense(100,activation='relu')(hidden2)
output=Dense(1, activation='relu')(hidden2_1)

encoder=Model(input,hidden2)
model = Model(input,output)
my_opti=optimizers.rmsprop(decay=0.0000001)
model.compile(loss='mean_squared_error', optimizer='rmsprop')
val=1000000
preval=val*2
callback = [
        EarlyStopping(monitor='val_loss', patience=2, min_delta=0.0000001, verbose=0)
    ]

model.fit(X_train, Y_train, epochs=20)
train_add=predict_state(encoder,model,train_add)
train = getTrain(input_shift, train_add)
X_train = train[ref.h_index + ref.x_index].values
Y_train=train[Target]
for i in range(40):
    #if(abs(preval-val)<1):
    #    break
    his=model.fit(X_train, Y_train, epochs=1, verbose=2)
    val_loss=his.history['loss']
    preval=val
    val=val_loss[-1]
    train_add=predict_state(encoder,model,train_add)
    train = getTrain(input_shift, train_add)
    X_train = train[ref.h_index + ref.x_index].values

    ############get every time loss######################
    loss_train.append(val)
    test_add = pd.read_csv(conf.intermediate_dir + 'test_add.csv')
    test_result = predict_result(encoder, model, test_add)
    test_add = pd.read_csv(conf.intermediate_dir + 'test_add.csv')
    loss=evaluateRegression(test_add, test_result)[0][1]
    loss_test.append(loss)
    ##validation
    test_add = pd.read_csv(conf.intermediate_dir + 'val_add.csv')
    test_result = predict_result(encoder, model, test_add)
    test_add = pd.read_csv(conf.intermediate_dir + 'val_add.csv')
    loss = evaluateRegression(test_add, test_result)[0][1]
    loss_validation.append(loss)
    '''
    test_add = pd.read_csv(conf.intermediate_dir + 'train_add.csv')
    test_result = predict_result(encoder, model, test_add)
    test_add = pd.read_csv(conf.intermediate_dir + 'train_add.csv')
    loss = evaluateRegression(test_add, test_result)[0][1]
    loss_true_train.append(loss)
    '''

print(loss_train)
print(loss_test)
print(loss_validation)
print(loss_true_train)

test_add=pd.read_csv(conf.intermediate_dir+'test_add.csv')
test_result=predict_result(encoder,model,test_add)
test_add=pd.read_csv(conf.intermediate_dir+'test_add.csv')
evaluateRegression(test_add,test_result)
test_result.to_csv(conf.result_dir+'test_predict.csv')

val_add=pd.read_csv(conf.intermediate_dir+'val_add.csv')
val_result=predict_result(encoder,model,val_add)
try:
    val_predict=pd.read_csv(conf.intermediate_dir+'val_predict.csv')
    val_predict[Target]=val_result[Target]
    val_predict.to_csv(conf.result_dir+'val_predict.csv',index=False)
except:
    val_result[['PTID_Key',Target]].to_csv(conf.result_dir+'val_predict.csv',index=False)