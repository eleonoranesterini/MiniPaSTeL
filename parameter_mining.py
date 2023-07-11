#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os

import function as fun
import fun_BinarySearch as fun_BS
import fun_ExploreGrid as fun_EG
import function_plots as fun_plot
import fun_classifcation as fun_cl
import specs_rtamt as sr



def SaveResultsToCSV(V, i ,sed):
    
   '''The function stores the values in V.tensor a CSV file'''
   
   if not os.path.exists('results'): os.mkdir('results')
   if not os.path.exists(f'results/seed_{sed}'): os.mkdir(f'results/seed_{sed}')
   
   path = f'results/seed_{sed}/'
   
   #Save V
   my_df = pd.DataFrame(V.tensor)
   my_df.to_csv(f'{path}V{i}_tensor_seed{sed}.csv', index=False, header=False)
   
   return


def main(inputs):
    
    # STEP 1: INITIALIZATION
    
    sed = inputs.seed
    np.random.seed(sed)
    
    traces = inputs.traces
    
    p_formula = inputs.p_formula
    par_bounds = inputs.par_bounds
    gran = inputs.granularity 
    sampling_freq = inputs.sampling_freq
    bool_mono = inputs.bool_mono
    mono = inputs.mono
    bool_binarysearch = inputs.bool_binarysearch 
    bool_quantitative = inputs.bool_quantitative
    constant_definition = inputs.constant_definition
    
    percentage_training = inputs.percentage_training
    n_train = inputs.numb_train
    bool_domain_knowledge = inputs.bool_domain_knowledge
    
    bool_plot_figure = inputs.bool_plot_figure
    bool_store_results = inputs.bool_store_results
    bool_different_templates =inputs.bool_different_templates
    
    file_name = inputs.file_name
    
    if bool_different_templates: 
        p_formula2 = inputs.p_formula2
        par_bounds2 = inputs.par_bounds2
        gran2 = inputs.granularity2 
        sampling_freq2 = inputs.sampling_freq2
        bool_mono2 = inputs.bool_mono2
        mono2 = inputs.mono2
        bool_binarysearch2 = inputs.bool_binarysearch2 
        bool_quantitative2 = inputs.bool_quantitative2
        constant_definition2 = inputs.constant_definition2
    
   
    if n_train is None:
        n_train = []
        n_train.append(int(len(traces[0])* percentage_training/100)  )
        n_train.append(int(len(traces[1])* percentage_training/100) )
        if len(traces) > 2: n_train.append(int(len(traces[2])* percentage_training/100))
    
    time_series_class1_train = traces[0][:n_train[0]]
    time_series_class1_test =  traces[0][n_train[0]:]
    
    time_series_class2_train = traces[1][:n_train[1]]
    time_series_class2_test =  traces[1][n_train[1]:]
    
    # 3 classes
    if len(traces) > 2: 
     time_series_class3_train = traces[2][:n_train[2]]
     time_series_class3_test =  traces[2][n_train[2]:]

    # STEP 2: APPROXIMATION OF VALIDITY DOMAINS
    # Create Approximation for the validity domain (one for each class)
    if not bool_binarysearch and not bool_quantitative: #Binary satisfaction with fixed granularity
        # Approximate the parameter space
        grid = fun.CreateGrid(par_bounds, gran)    
        # Approximate the validity domain for class 1   
        if bool_mono: V1 = fun_EG.ExploreGridMonotonic( time_series_class1_train , 1,  grid, mono, p_formula, sampling_freq, constant_definition )
        else: V1 = fun_EG.ExploreGrid(time_series_class1_train, 1, grid, p_formula, sampling_freq,  constant_definition)   
        print('V1 done')
        
        # Approximate the validity domain for class 2
        if bool_mono: V2 = fun_EG.ExploreGridMonotonic( time_series_class2_train , 2,  grid, mono , p_formula, sampling_freq, constant_definition)
        else: V2 = fun_EG.ExploreGrid(time_series_class2_train, 2, grid, p_formula, sampling_freq, constant_definition)
        print('V2 done')
        
        if len(traces) > 2:
            if bool_mono: V3 = fun_EG.ExploreGridMonotonic( time_series_class3_train , 3,  grid, mono , p_formula, sampling_freq, constant_definition)
            else: V3 = fun_EG.ExploreGrid(time_series_class3_train, 3, grid, p_formula, sampling_freq, constant_definition)
            print('V3 done')
        
    elif bool_binarysearch and not bool_quantitative: #Binary satisfaction with binary search
        if bool_mono: V1 = fun_BS.BinarySearchMonotonic(time_series_class1_train,  gran, par_bounds,fun.Approx_Val(1, [ ]) , mono,  p_formula, sampling_freq, constant_definition)
        else: V1 = fun_BS.BinarySearch(time_series_class1_train,  gran , par_bounds,  fun.Approx_Val(1, [ ]), [],p_formula, sampling_freq, constant_definition)
        print('V1 done')
        if bool_mono: V2 = fun_BS.BinarySearchMonotonic(time_series_class2_train,  gran, par_bounds,fun.Approx_Val(2, [ ]) , mono,  p_formula, sampling_freq, constant_definition)
        else: V2 = fun_BS.BinarySearch(time_series_class2_train,  gran , par_bounds,  fun.Approx_Val(2, [ ]), [] ,p_formula, sampling_freq, constant_definition)
        print('V2 done')
        
        if len(traces)>2 :
            if bool_mono: V3 = fun_BS.BinarySearchMonotonic(time_series_class3_train,  gran, par_bounds, fun.Approx_Val(3, [ ]) , mono,  p_formula, sampling_freq, constant_definition)
            else:V3 = fun_BS.BinarySearch(time_series_class3_train,  gran , par_bounds,  fun.Approx_Val(3, [ ]), [] ,p_formula, sampling_freq, constant_definition)
            print('V3 done')
        
    elif not bool_binarysearch and bool_quantitative:  #Quantitative robustness with fixed granularity
        # Approximate the parameter space
        grid = fun.CreateGrid(par_bounds, gran)    
        # Approximate the validity domain for class 1   
        V1 = fun_EG.ExploreGridQuantitative(time_series_class1_train, 1, grid, p_formula, sampling_freq,  constant_definition)  
        print('V1 done')
        
        # Approximate the validity domain for class 2
        V2 = fun_EG.ExploreGridQuantitative(time_series_class2_train, 2, grid, p_formula, sampling_freq,  constant_definition)
        print('V2 done')
        
        if len(traces)>2 :
            V3 = fun_EG.ExploreGridQuantitative(time_series_class3_train, 3, grid, p_formula, sampling_freq, constant_definition)
            print('V3 done')
            
    elif bool_binarysearch and bool_quantitative: #Quantitative robusteness with binary search
        V1 = fun_BS.BinarySearchQuantitative(time_series_class1_train,  gran , par_bounds,  fun.Approx_Val(1, [ ]), [], p_formula, sampling_freq, constant_definition)
        print('V1 done')
        V2 = fun_BS.BinarySearchQuantitative(time_series_class2_train,  gran , par_bounds,  fun.Approx_Val(2, [ ]), [] , p_formula, sampling_freq, constant_definition)
        print('V2 done')
        
        if len(traces)>2 :
            V3 = fun_BS.BinarySearchQuantitative(time_series_class3_train,  gran , par_bounds,  fun.Approx_Val(3, [ ]), [] , p_formula, sampling_freq,constant_definition)
            print('V3 done')
        
    else: print('Error in the choice of the approach')
    
    
    if bool_store_results:
        SaveResultsToCSV(V1, 1, sed)
        SaveResultsToCSV(V2, 2, sed)
        if len(traces)>2 : SaveResultsToCSV(V3, 3, sed)
    
    if bool_different_templates:
        
        ## Repeat the approximation of validity domains with respect to the second formula template (TWO CLASSES, but similarly for multiple classes)
        if not bool_binarysearch2 and not bool_quantitative2: #Binary satisfaction with fixed granularity
            # Approximate the parameter space
            grid = fun.CreateGrid(par_bounds2, gran2)    
            # Approximate the validity domain for class 1   
            if bool_mono2: V1_2 = fun_EG.ExploreGridMonotonic( time_series_class1_train , 1,  grid, mono2, p_formula2, sampling_freq2 , constant_definition2)
            else: V1_2 = fun_EG.ExploreGrid(time_series_class1_train, 1, grid, p_formula2, sampling_freq2,  constant_definition2)   
            print('V1_2 done')
        
            # Approximate the validity domain for class 2
            if bool_mono2: V2_2 = fun_EG.ExploreGridMonotonic( time_series_class2_train , 2,  grid, mono2 , p_formula2, sampling_freq2, constant_definition2)
            else: V2_2 = fun_EG.ExploreGrid(time_series_class2_train, 2, grid, p_formula2, sampling_freq2, constant_definition2)
            print('V2_2 done')
            
        elif bool_binarysearch2 and not bool_quantitative2: #Binary satisfaction with binary search
            V1_2 = fun_BS.BinarySearch(time_series_class1_train,  gran2 , par_bounds2,  fun.Approx_Val(1, [ ]), [],p_formula2, sampling_freq2, constant_definition2)
            print('V1_2 done')
            V2_2 = fun_BS.BinarySearch(time_series_class2_train,  gran2 , par_bounds2,  fun.Approx_Val(2, [ ]), [] ,p_formula2, sampling_freq2, constant_definition2)
            print('V2_2 done')
            
        elif not bool_binarysearch2 and bool_quantitative2:  #Quantitative robustness with fixed granularity
            # Approximate the parameter space
            grid = fun.CreateGrid(par_bounds2, gran2)    
            # Approximate the validity domain for class 1   
            V1_2 = fun_EG.ExploreGridQuantitative(time_series_class1_train, 1, grid, p_formula2, sampling_freq2, constant_definition2)  
            print('V1_2 done')
            
            # Approximate the validity domain for class 2
            V2_2 = fun_EG.ExploreGridQuantitative(time_series_class2_train, 2, grid, p_formula2, sampling_freq2, constant_definition2)
            print('V2_2 done')
                
        elif bool_binarysearch2 and bool_quantitative2: #Quantitative robusteness with binary search
            V1_2 = fun_BS.BinarySearchQuantitative(time_series_class1_train,  gran2 , par_bounds2,  fun.Approx_Val(1, [ ]), [], p_formula2, sampling_freq2, constant_definition2)
            print('V1_2 done')
            V2_2 = fun_BS.BinarySearchQuantitative(time_series_class2_train,  gran2 , par_bounds2,  fun.Approx_Val(2, [ ]), [] , p_formula2, sampling_freq2, constant_definition2)
            print('V2_2 done')
            
        else: print('Error in the choice of the approach')
        
        if bool_store_results:
            SaveResultsToCSV(V1_2, '1_formula2', sed)
            SaveResultsToCSV(V2_2, '2_formula2', sed)
        
        
    ## STEP 3: EXTRACT PARAMETERS    
    if not bool_different_templates:
        
        #Two classes
        if len(traces) == 2:
            if bool_binarysearch: V1, V2 = fun_BS.AdaptGranularities(V1, V2, 2)
            if bool_domain_knowledge: parameters = fun.ExtractParameters_DOMAIN_KNOWLEDGE(V1, V2)
            elif not bool_quantitative: parameters = fun.ExtractParameters(V1, V2, sed)
            elif bool_quantitative:
                parameters = []
                parameters.append(fun.ExtractParametersQuantitative(V1, V2) ) #point in V1 for class1 
                parameters.append(fun.ExtractParametersQuantitative(V2, V1) ) #point in V2 for class 2
            
            parameter1 = fun.round_timing_parameters(parameters[0], sampling_freq, p_formula)
            parameter2 = fun.round_timing_parameters(parameters[1], sampling_freq, p_formula)
      
            formula1 = sr.instantiate_formula(p_formula, parameter1 )
            formula2 = sr.instantiate_formula(p_formula, parameter2)
            
            print('STL formula for class 1: ' , formula1 )
            print('STL formula for class 2: ' , formula2 )
            
            with open(f'{file_name}','a') as file: file.write(f'\n\nSTL formula for class 1: {formula1}' )
            with open(f'{file_name}','a') as file: file.write(f'\nSTL formula for class 2: {formula2}' )

            
        # 3 classes
        if len(traces) > 2:
            if bool_binarysearch : 
                 V1, V2 = fun_BS.AdaptGranularities(V1, V2, 2)
                 V1, V3 = fun_BS.AdaptGranularities(V1, V3, 3)
                 V2, V3 = fun_BS.AdaptGranularities(V2, V3, 3)
                
            if not bool_quantitative:
                
                parameters = []
                # V1 vs (V2 union V3)
                parameters.append(fun.ExtractParametersMultiple(V1, V2, V3, sed, bool_mono, mono))
                # V2 vs (V1 union V3)
                parameters.append(fun.ExtractParametersMultiple(V2, V1, V3, sed, bool_mono, mono))
                # V3 vs (V1 union V2)
                parameters.append(fun.ExtractParametersMultiple(V3, V1, V2, sed, bool_mono, mono))
            
                parameter1 = fun.round_timing_parameters(parameters[0][0], sampling_freq, p_formula)
                parameter2 = fun.round_timing_parameters(parameters[1][0], sampling_freq, p_formula)
                parameter3 = fun.round_timing_parameters(parameters[2][0], sampling_freq, p_formula)
            
            
            elif bool_quantitative:
                parameters = []
                # V1 vs (V2 union V3)
                parameters.append(fun.ExtractParametersQuantitativeMultiple(V1, V2,  V3))
                # V2 vs (V1 union V3)
                parameters.append(fun.ExtractParametersQuantitativeMultiple(V2, V1,  V3))
                # V3 vs (V1 union V2)
                parameters.append(fun.ExtractParametersQuantitativeMultiple(V3, V1,  V2))
                
            
                parameter1 = fun.round_timing_parameters(parameters[0], sampling_freq, p_formula)
                parameter2 = fun.round_timing_parameters(parameters[1], sampling_freq, p_formula)
                parameter3 = fun.round_timing_parameters(parameters[2], sampling_freq, p_formula)
            
            
            formula1 = sr.instantiate_formula( p_formula , parameter1 )
            formula2 = sr.instantiate_formula( p_formula , parameter2 )
            formula3 = sr.instantiate_formula( p_formula , parameter3 )
            
            print('STL formula for class 1: ' , formula1 )
            print('STL formula for class 2: ' , formula2 )
            print('STL formula for class 3: ' , formula3 )
            
            with open(f'{file_name}','a') as file: file.write(f'\n\nSTL formula for class 1: {formula1}' )
            with open(f'{file_name}','a') as file: file.write(f'\nSTL formula for class 2: {formula2}' )
            with open(f'{file_name}','a') as file: file.write(f'\nSTL formula for class 3: {formula3}' )
        
    elif bool_different_templates:
        
        if bool_binarysearch: V1, V2 = fun_BS.AdaptGranularities(V1, V2, 2)
        if not bool_quantitative: parameters = fun.ExtractParameters(V1, V2, sed)
        elif bool_quantitative:
            parameters = []
            parameters.append(fun.ExtractParametersQuantitative(V1, V2) ) #point in V1 for class1 
        
        parameter1 = fun.round_timing_parameters(parameters[0], sampling_freq, p_formula)
        formula1 = sr.instantiate_formula(p_formula, parameter1)
        
        print('STL formula for class 1: ' , formula1 )
        with open(f'{file_name}','a') as file: file.write(f'\n\nSTL formula for class 1: {formula1}' )
            
        
        if bool_binarysearch2: V1_2, V2_2 = fun_BS.AdaptGranularities(V1_2, V2_2, 2)
        if not bool_quantitative2: parameters2 = fun.ExtractParameters(V1_2, V2_2, sed)
        elif bool_quantitative2:
            parameters2 = []
            parameters2.append(['a'])#skip the first component
            parameters2.append(fun.ExtractParametersQuantitative( V2_2, V1_2) ) #point in V2_2 for class2
        
        parameter2 = fun.round_timing_parameters(parameters2[1], sampling_freq, p_formula2)
        formula2 = sr.instantiate_formula(p_formula2, parameter2)
        print('STL formula for class 2: ' , formula2 )
        with open(f'{file_name}','a') as file: file.write(f'\nSTL formula for class 2: {formula2}' )
            
    
    
    ## STEP 4: EVALUATE MISC
    
    if len(traces) == 2:
        if not bool_different_templates : 
            sampling_freq2 = sampling_freq
            constant_definition2 = constant_definition
        MSC_train, precision_train, recall_train = fun_cl.EvaluateMCR_2classes(time_series_class1_train, time_series_class2_train, formula1,  formula2 , sampling_freq, sampling_freq2, constant_definition, constant_definition2 )
        
        
        with open(f'{file_name}','a') as file: 
            file.write(f'\n\n\nMSC_train: {MSC_train}' )
            file.write(f'\nprecision_train: {precision_train}' )
            file.write(f'\nrecall_train: {recall_train}' )
            
            
    
        if len(time_series_class1_test)>0 :
            MSC_test, precision_test, recall_test =  fun_cl.EvaluateMCR_2classes(time_series_class1_test, time_series_class2_test, formula1,  formula2 , sampling_freq, sampling_freq2, constant_definition, constant_definition2)
            with open(f'{file_name}','a') as file: 
                file.write(f'\n\n\nMSC_test: {MSC_test}' )
                file.write(f'\nprecision_test: {precision_test}' )
                file.write(f'\nrecall_test: {recall_test}' )

    elif len(traces)>2: 
        
        confusion_matrix = False
        
        MSC1_train, precision1_train, recall1_train , MSC2_train, precision2_train, recall2_train, MSC3_train, precision3_train, recall3_train \
         = fun_cl.EvaluateMCR_3classes(time_series_class1_train, time_series_class2_train, time_series_class3_train ,formula1, formula2, formula3, sampling_freq, constant_definition, confusion_matrix )
        
        with open(f'{file_name}','a') as file: 
            file.write(f'\n\n\nMSC1_train: {MSC1_train}\nMSC2_train: {MSC2_train}\nMSC3_train: {MSC3_train}\n' )
            file.write(f'\nprecision1_train: {precision1_train}\nprecision2_train: {precision2_train}\nprecision3_train: {precision3_train}\n' )
            file.write(f'\nrecall1_train: {recall1_train}\nrecall2_train: {recall2_train}\nrecall3_train: {recall3_train}\n' )
        
        if len(time_series_class1_test)>0 :
            MSC1_test, precision1_test, recall1_test , MSC2_test, precision2_test, recall2_test, MSC3_test, precision3_test, recall3_test \
         = fun_cl.EvaluateMCR_3classes(time_series_class1_test, time_series_class2_test, time_series_class3_test ,formula1, formula2, formula3, sampling_freq , constant_definition, confusion_matrix)
            with open(f'{file_name}','a') as file: 
                file.write(f'\n\n\nMSC1_test: {MSC1_test}\nMSC2_test: {MSC2_test}\nMSC3_test: {MSC3_test}\n' )
                file.write(f'\nprecision1_test: {precision1_test}\nprecision2_test: {precision2_test}\nprecision3_test: {precision3_test}\n' )
                file.write(f'\nrecall1_test: {recall1_test}\nrecall2_test: {recall2_test}\nrecall3_test: {recall3_test}\n' )
        

    ## STEP 5: PLOT
    if bool_plot_figure:
        
        if not bool_different_templates:
            if len(traces) == 2: fun_plot.plot_validity_domains(par_bounds, V1, V2, [ parameter1, parameter2 ], bool_quantitative , None)
            # 3 classes plot only non-quantitative
            # elif not bool_quantitative: fun_plot.plot_validity_domains(par_bounds, V1, V2,  [ parameter1, parameter2 , parameter3], bool_quantitative , V3)
        
        elif bool_different_templates:
            
            fun_plot.plot_validity_domains(par_bounds, V1, V2,  [parameter1,parameter1], bool_quantitative , None)
            
            fun_plot.plot_validity_domains(par_bounds2, V1_2, V2_2,  [parameter2,parameter2] , bool_quantitative2 , None)
            
    