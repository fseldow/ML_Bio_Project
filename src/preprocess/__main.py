import pandas as pd
import conf as conf
import os
from src.preprocess.input_handle import auto_compen,cor_compen,final_drop,normalization
from src.preprocess.other_handle import shift_datas


def preprocess(start_point=0):
    df = pd.read_csv(conf.raw_dir + 'TADPOLE_InputData.csv')
    if os.path.isfile(conf.raw_dir+'TADPOLE_InputData.csv')==False:
        print('original input file cannot found')
        exit(-1)
    if os.path.isfile(conf.intermediate_dir+'auto_com.csv')==False or start_point<=conf.START_FROM_AUTO:
        df=auto_compen()
    if os.path.isfile(conf.intermediate_dir+'cor_com.csv')==False or start_point<=conf.START_FROM_COR:
        df=cor_compen(df,start_point==conf.START_FROM_COR)
    if os.path.isfile(conf.intermediate_dir+'final_drop.csv')==False or start_point<=conf.START_FROM_DROP:
        df=final_drop(df,start_point==conf.START_FROM_DROP)
    if os.path.isfile(conf.intermediate_dir+'norm.csv')==False or start_point<=conf.START_FROM_NORM:
        df=normalization(df,start_point==conf.START_FROM_NORM)
    if start_point<=conf.START_FROM_SHIFT:
        if start_point<=conf.START_FROM_NORM:
            start_point=conf.START_FROM_SHIFT
        df=shift_datas(input_flag=(start_point&conf.SHIFT_INPUT>0),
                       train_flag=(start_point&conf.SHIFT_TRAIN>0),
                       test_flag=(start_point&conf.SHIFT_TEST>0),
                       validation_flag=(start_point&conf.SHIFT_VALIDATION>0))