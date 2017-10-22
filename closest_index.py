import re
import pandas as pd
def normalization(bf,data_df):
    for item in data_df:
        if item=='PTID_Key':
            continue
        try:
            bf[item]=(bf[item]-bf[item].mean(axis=0))/(bf[item].max(axis=0)-bf[item].min(axis=0))
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
