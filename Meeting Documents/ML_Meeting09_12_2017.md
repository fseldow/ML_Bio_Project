# ML Meeting 09/12/2017
## Data Files
**Dictionary:** parameter explaination.  
**InputData:** The data of patient infromation.  
**PredictTargetData_valid:** The eventual test need to assign.   
**test:** Data used to test our model.  
**train:** Data used to train our model.
## Procedure
1. Extract the feature vector(fv) of every ptid in *input_data.csv*.
2. <font color=blue>(Train start)</font> Accroding to the ptid in *train.csv*, get the fv.
3. Import the fv into Model.
4. Combine date in *train.csv* to get result of *DX, ADAS13, Ventricles_Norm or MMSE*
5. Calculate the cost according to the loss function.
6. Repeat 3-5 to **adjust the model** to minimize the cost. <font color=blue>(End Train)</font>
7. Repeat 2-5, but the data source is *test.csv* instead of *train.csv*. By this way, we can test the precision of our model.
8. If successful, we can take the same way as 7 in *valid.csv* as our assignment.
## Problem to solve
1. How to handle the missing data.
2. How to extract the **feature vector** from *input_data.csv*.  <font color=red>Emergency!</font>
    > Which sets of data are useful  
    > 
3. Select which kind of **training model**:  
    > SVM? Deep learning? or anything else.  
    > How to build **Loss Function**
4. Prediction Problem:  
    >[1,2,3,4]=F[f(PTID),date]
5. The analysis of *Diction.csv*
## Potential solution
1. TBD
2. Refer to related the journals. <font color=red>(The most essential work in purposal)</font>
3. We sperate the problem into 2 subproblems. The first is about **DX(CN,AD,MCI)** judgement. The second is about prediction of **ADAS13, Ventricles_Norm & MMSE**.
   + _Subproblem 1_:  
       <font color=red>Attention: It is classification of ternary</font>  
       **Ternary Classification** :Leverage **SVM** for every pair of them and then combine the boundaries.  
       **Loss Function** could temporaily use **ML** with regulization.
   + _Subproblem 2_:  
       **Deep Learning**?  
       **Sum of squared differnce(ssd)**?
4. Still refer to journals or even change a method. NOT EMERGENCY
5. Take time to look up the parameter online or ask TA for help. Priority after or same as 2.
##Things to do in purposal:
+ <font color=red>ATTENTION: NO LONGER THAN 2 PAGES</font>
+ Team member names.
+ Chosen dataset & machine learning problem  
    >which project we chose  
+ A basic literature survey. <font color=red>Main work this week</font>  
    >**How to extract fv**  
    >Select which dataset in *input_data.csv*  
    >How could we link a patient to other patients with similar body feature.
+ Planned machine learning strategy
    >As what mentioned in _Potential Solution\_3_
+ Baseline approaches
    >Refer to procedure
