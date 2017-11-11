import os


def history_recall(PTID):
	


print('test')
train_object=open('C:\Users\Tycho\Desktop\ML_BME_5970\Tadpole-Data\public\TADPOLE_TargetData_train.csv')
line=train_object.readline()
firstline=True
while line:
	linevalue=line.split(',')
	if (firstline=True):
		firstline=False
		continue
'''
train_object.readline()	
'''
	history_recall(linevalue[1])