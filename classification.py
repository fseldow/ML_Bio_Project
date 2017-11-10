import pandas as pd
import X_Y_H as ref
from keras.models import  Model
from keras.layers import Dense, Input,Dropout
from keras.models import Sequential
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
import csv_utils as utils
import numpy as np
from evaluate_baseline import evaluateRegression
from evaluate_baseline import evaluateClassification
import sklearn
import keras


Target='DXCHANGE'
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
        print(i, 'in', len(target_df.index))
        id = target_df['PTID_Key'][i]
        start_in_train = target_dict[id][0]
        end_in_train = target_dict[id][1]
        if i != start_in_train:
            X_test = target_df.loc[i - 1, ref.h_index + ref.x_index].as_matrix(columns=None)
            temp = Encoder.predict(np.expand_dims(X_test, axis=0))
            for j in range(len(ref.h_index)):
                target_df.set_value(i, ref.h_index[j], temp[0, j])
    return target_df

def getTrain(input_df,train_df):
    train=pd.concat((input_df,train_df))
    #train=train.sort_values(by=['PTID_Key','M'])
    #train.index = pd.RangeIndex(len(train.index))
    #train=utils.dataCompen(train,Target)
    train = train.dropna(axis=0, subset=[Target])
    return train



#########################################################################
epochs=10

input_shift=pd.read_csv('input_shift.csv')
train_add=pd.read_csv('train_add.csv')
input_shift['DXCHANGE']=input_shift['DXCHANGE']-1
train_add['DXCHANGE']=train_add['DXCHANGE']-1
train=getTrain(input_shift,train_add)


X_train=train[ref.h_index+ref.x_index].values

Y_train=train[Target].values
Y_train=keras.utils.to_categorical(Y_train, 3)

input=Input(shape=(X_train.shape[1],))
hidden1=Dense(30, activation='relu')(input)
hidden1_11=Dense(15,activation='sigmoid')(hidden1)
hidden1_1=Dense(20, activation='relu')(hidden1_11)
hidden2=Dense(len(ref.h_index),activation='relu')(hidden1_1)
output=Dense(3, activation='softmax')(hidden2)

encoder=Model(input,hidden2)
model = Model(input,output)

model.compile(loss='categorical_crossentropy', optimizer='Adam',metrics=['accuracy'])
val=1000000
preval=val*2

for i in range(30):
    if (abs(preval - val) < 5):
        break
    callback = [
        EarlyStopping(monitor='val_loss', patience=2, min_delta=0.01, verbose=0)
    ]
    his=model.fit(X_train, Y_train, epochs=20, verbose=1,callbacks=callback,validation_split=0.1)
    val_loss = his.history['val_loss']
    preval = val
    val = val_loss[-1]
    train_add = predict_state(encoder, model, train_add)
    train = getTrain(input_shift, train_add)
    X_train = train[ref.h_index + ref.x_index].values

test_add=pd.read_csv('val_add.csv')
test_add[Target]=test_add[Target]-1
test_complete=predict_state(encoder,model,test_add)
#test_complete=test_complete.dropna(subset=[Target],axis=0)
#test_complete.index=range(len(test_complete.index))
X_test=test_complete[ref.h_index+ref.x_index].values
Y_test=test_complete[Target].values
#Y_test=keras.utils.to_categorical(Y_test, 3)

result=model.predict(X_test)
np.savetxt('result_test_classi.csv',result, delimiter=',')
np.savetxt('result_test_classi2.csv',Y_test, delimiter=',')
'''
test_add=pd.read_csv('test_add.csv')
evaluateClassification(test_add,test_result)
test_result.to_csv('test_predict.csv')
'''