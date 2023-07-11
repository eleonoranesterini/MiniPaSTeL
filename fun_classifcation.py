#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:39:24 2023

@author: elo
"""
import numpy as np
import pandas as pd
import specs_rtamt as sr
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def EvaluateMCR_2classes(time_series_class1, time_series_class2,  formula1,  formula2 , sampling_freq, sampling_freq2, constant_definition, constant_definition2):
    

    # y_true = [1]* len(time_series_class1)+ [2]* len(time_series_class2) 
    
    TP = 0
    TN = 0
    FN = 0
    FP = 0
    
 
    y_pred = []
    
    robS1= []
    
    for index in range(len(time_series_class1)):
        
          robS1_param1 = sr.EvaluateRob( time_series_class1[index] , formula1 , sampling_freq, constant_definition )
          robS1_param2 = sr.EvaluateRob( time_series_class1[index] , formula2 , sampling_freq2, constant_definition2 )
          robS1 = np.argmax([robS1_param1, robS1_param2])+1 #
          
          print('rob1', robS1)
          y_pred.append(robS1)
          
          if robS1 == 1:   TP += 1
          
          elif robS1 == 2:   FN += 1
              
          else: print('err1')
          
    robS2 = []
    
    for index in range(len(time_series_class2)):
         robS2_param1 = sr.EvaluateRob(time_series_class2[index], formula1 , sampling_freq, constant_definition)
         robS2_param2 = sr.EvaluateRob(time_series_class2[index], formula2 , sampling_freq2, constant_definition2)
         
         robS2 = np.argmax([robS2_param1, robS2_param2])+1 #,
         y_pred.append(robS2)
         
         print('rob2', robS2)
         
         if robS2 == 2:  TN += 1
         
         elif robS2 == 1:  FP += 1
             
         else: print('err2')
    
   
    
    MSC = ((FN + FP) / (FN+ FP + TP +TN))
    if ( TP +FP) !=0 : precision = (TP / ( TP +FP))
    else: precision = np.inf
    
    if (TP + FN)!= 0: recall = (TP /(TP + FN))
    else: recall = np.inf
        
    return MSC, precision, recall


def EvaluateMCR_other_tools(time_series_class1, time_series_class2,  time_series_class3, formula,  sampling_freq):
    

    # y_true = [1]* len(time_series_class1)+ [2]* len(time_series_class2) 
    
    TP = 0
    TN = 0
    FN = 0
    FP = 0
    
    for i, el in enumerate(time_series_class1):
        
          rob = sr.EvaluateRob( el  , formula , sampling_freq, [ ] ) #[8, 'float']
          # print(rob)
          if rob >= 0 :   TP += 1
              
          else: FN += 1

          
    
    for el in time_series_class2:
         rob = sr.EvaluateRob(el , formula , sampling_freq,  [ ] )#[8, 'float']
         
         # print('2',rob)
         if rob >= 0:  FP += 1
             
         else: TN += 1
         
    for el in time_series_class3:

          rob = sr.EvaluateRob(el , formula , sampling_freq, [])
         
         
          if rob >= 0:  FP += 1
             
          else: TN += 1
    
   
    
    MSC = ((FN + FP) / (FN+ FP + TP +TN))
    if ( TP +FP) !=0 : precision = (TP / ( TP +FP))
    else: precision = np.inf
    
    if (TP + FN)!= 0: recall = (TP /(TP + FN))
    else: recall = np.inf
        
    print(MSC, FN+ FP + TP +TN)
    
    return MSC, precision, recall


def EvaluateMCR_3classes(time_series_class1, time_series_class2, time_series_class3 ,formula1,formula2, formula3, sampling_freq, constant_definition, fig ):

    y_true = [1]* len(time_series_class1)+ [2]* len(time_series_class2) + [3]* len(time_series_class3)
    
    robS1 = []
    TP1 = 0
    TP2 = 0
    TP3 = 0
    
    FP1 = 0
    FP2 = 0
    FP3 = 0
    
    TN1 = 0
    TN2 = 0
    TN3 = 0
    
    FN1 = 0
    FN2 = 0
    FN3 = 0
    
    y_pred = []
    
    for index in range(len(time_series_class1)):
          robS1_param1 = sr.EvaluateRob( time_series_class1[index] ,   formula1, sampling_freq, constant_definition)
          robS1_param2 = sr.EvaluateRob( time_series_class1[index] ,   formula2, sampling_freq, constant_definition)
          robS1_param3 = sr.EvaluateRob( time_series_class1[index] ,   formula3, sampling_freq, constant_definition)
          robS1 = np.argmax([robS1_param1, robS1_param2, robS1_param3])+1 #
          
          y_pred.append(robS1)
          
          if robS1 == 1: 
              TP1 += 1
              TN2 += 1
              TN3 += 1
          
          elif robS1 == 2: 
              FP2 += 1
              FN1 += 1
              TN3 += 1
              
          elif robS1 == 3:
              FN1 += 1
              FP3 += 1
              TN2 += 1
          else: print('err1')
        
     
      
    robS2 = []
    for index in range(len(time_series_class2)):
         robS2_param1 = sr.EvaluateRob(np.array(time_series_class2[index]), formula1, sampling_freq, constant_definition)
         robS2_param2 = sr.EvaluateRob(np.array(time_series_class2[index]), formula2, sampling_freq , constant_definition)
         robS2_param3 = sr.EvaluateRob(np.array(time_series_class2[index]), formula3, sampling_freq, constant_definition)
         
         robS2= np.argmax([robS2_param1, robS2_param2, robS2_param3])+1 #,
         y_pred.append(robS2)
         
         if robS2 == 2: 
             TP2 += 1
             TN1 += 1
             TN3 += 1
         
         elif robS2 == 1: 
            FP1 += 1
            FN2 += 1
            TN3 += 1
            
         elif robS2 == 3:
            FN2 += 1
            FP3 += 1
            TN1 += 1
         else: print('err2')
         
    robS3 = []
    for index in range(len(time_series_class3)):
          robS3_param1 = sr.EvaluateRob( np.array(time_series_class3[index]),  formula1, sampling_freq, constant_definition)
          robS3_param2 = sr.EvaluateRob( np.array(time_series_class3[index]),  formula2, sampling_freq, constant_definition)
          robS3_param3 = sr.EvaluateRob( np.array(time_series_class3[index]),  formula3, sampling_freq, constant_definition)
          
          robS3 = np.argmax([robS3_param1, robS3_param2,  robS3_param3])+1  #,
          y_pred.append(robS3)
          
          if robS3 == 3: 
              TP3 += 1
              TN1 += 1
              TN2 += 1
          
          elif robS3 == 2: 
              FP2 += 1
              FN3 += 1
              TN1 += 1
              
              
          elif robS3 == 1:
              
              FP1 += 1
              TN2 += 1
              FN3 += 1
              
              
          else: print('err3')
          

    MSC1 = ((FN1 + FP1) / (FN1+ FP1 + TP1 +TN1))
    if ( TP1 +FP1) !=0: P1 = (TP1 / ( TP1 +FP1) )
    else: P1 = np.inf
    
    if (TP1 + FN1)!=0: R1 = (TP1 /(TP1 + FN1))
    else: R1 = np.inf
    
    
    MSC2 = ((FN2 + FP2) / (FN2+ FP2 + TP2 +TN2))
    if ( TP2 +FP2) !=0: P2 = (TP2 / ( TP2 +FP2) )
    else: P2 = np.inf
    if (TP2 + FN2)!=0: R2 = (TP2 /(TP2 + FN2))
    else: R2 = np.inf
    
    MSC3 = ((FN3 + FP3) / (FN3+ FP3 + TP3 +TN3))
    if ( TP3 +FP3) !=0: P3 = (TP3 / ( TP3 +FP3) )
    else: P3 = np.inf
    if (TP3 + FN3)!=0: R3 = (TP3 /(TP3 + FN3))
    else: R3 = np.inf
    
    plt.close()
    if fig:
        conf_matrix = confusion_matrix(y_true, y_pred)
        df_conf = pd.DataFrame(conf_matrix, index = ['1', '2', '3'], columns=['1', '2', '3'])
        plt.figure(figsize=(6,4))
        sns.heatmap(df_conf, annot=True)
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(f'confusion_matrix.pdf', format='pdf')
        plt.close()

    return MSC1, P1, R1, MSC2, P2, R2, MSC3 , P3, R3