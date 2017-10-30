import pandas as pd
shift=pd.read_csv('input_shift.csv')
a1=[1,7,9]
a2=[2,4,8]
a3=[3,5,6]
for i in range(len(shift)):
   if shift['DXCHANGE'][i] in a1:
       shift.set_value(i,'DXCHANGE',1)
   if shift['DXCHANGE'][i] in a2:
       shift.set_value(i, 'DXCHANGE', 2)
   if shift['DXCHANGE'][i] in a3:
       shift.set_value(i, 'DXCHANGE', 3)
shift.to_csv('input_shift.csv',index=None)
shift=pd.read_csv('../input_normalization.csv')
a1=[1,7,9]
a2=[2,4,8]
a3=[3,5,6]
for i in range(len(shift)):
   if shift['DXCHANGE'][i] in a1:
       shift.set_value(i,'DXCHANGE',1)
   if shift['DXCHANGE'][i] in a2:
       shift.set_value(i, 'DXCHANGE', 2)
   if shift['DXCHANGE'][i] in a3:
       shift.set_value(i, 'DXCHANGE', 3)
shift.to_csv('../input_normalization.csv',index=None)
