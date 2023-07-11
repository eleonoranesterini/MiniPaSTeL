#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Explore Grid functions:
    - ExploreGrid (binary satisfaction)
    - ExploreGridQuantitative (quantitative robustness)
    - ExploreGridMonotonic(when monotonicity holds)
"""
import numpy as np
import itertools
import specs_rtamt as sr
import function as fun

def ExploreGrid( time_series , label,  grid ,p_formula, sampling_freq, constant_definition):
    
    ''' The function computes the satisfaction or not of each cell of the parameter space
        associated to a PSTL template and a class of time series.
        
        Given a cell, r samples (parameters valuations) are uniformly picked inside of it.
        Each trace is evaluate against every parameters valuation: 
            If A SINGLE trace do NOT satisfy that parameter valuation, than NON SATISFACTION is associated to that PARAMETER VALUATION.
            If ALL TRACES satisfy that parameter valuation, than SATISFACTION is associated to that PARAMETER VALUATION.
            
        Each cell is associated to r valuaes of satisfaction. 
            If at least half of them are SATSIFIED, then the CELL is associated to SATISFACTION,
            otherwise the cell is associated with non satisfaction.
        
    
        INPUT: 
           - time series : set of time series associated with a single label
           - label : label of the class
           - grid:  parameters partition grid returned by CreateGrid()
           - p_formula : parametric_formula
           - sampling_freq: list of two elements
           
        
        OUTPUT:
           - binary tensor : list of parameters valuation and labels (satisfaction or not). It has as
            lenght the cardinality of the cartesian product of the parameters partitions.
            Binary tensor = [ [-], [-], .. ,[-] ] where [-] has lenght = number of parameters + 1 (s, satisfaction)
            [-] = parameters valuation for which the satisfaction is evaluated
       
    '''
    
    binary_tensor = []
    
    nb_parameters = len(grid.tensor)
    
    parameters_step = [list(np.arange(len(grid.tensor[par]))) for par in range(nb_parameters)]
    
    #number of valuations in each cell: r 
    r = 99 #alpha = 0.05, p_0 = 0.03

    
    #Cartesian product of all combination of parameters
    #Describe each cell with a vector in [0,1]^nb_parameters 
    for iprod_car in itertools.product(*parameters_step): # i.e., for each cell
        parameters_list = list(iprod_car)
        
        #Random uniform sampling 
        parameters_min = [ grid.tensor[par][parameters_list[par]][0] for par in range(nb_parameters)]
        parameters_max = [ grid.tensor[par][parameters_list[par]][1] for par in range(nb_parameters)]
        
        random_par = np.random.uniform(low=parameters_min, high=parameters_max, size=(r,nb_parameters))
        
        
        rho = [] #List that will be long r and that represents the satisfaction 
        
        #Loop of parameters valuation samples in a single cell
        for i in range(r): 
            parameters_valuation = random_par[i]
    
            parameters_valuation = fun.round_timing_parameters(parameters_valuation, sampling_freq, p_formula)
            
            #Loop to evaluate the satisfaction of a single parameter valuation
            for j, x in enumerate(time_series):
                # Call tool rtamt to get robustness of trace x with respect to parameters paremeters_valuation
                formula = sr.instantiate_formula(p_formula, parameters_valuation)
                rob_single_time_series = sr.EvaluateRob(x, formula, sampling_freq, constant_definition)
                
                # If ONE time-series do NOT satisfy, than the parameter valuation is associated with -1
                if rob_single_time_series=='undef' or rob_single_time_series < 0: 
                    rho.append(-1)
                    break
                
                # If ALL time series satisfy, then the parameter valuation is associated with 1   
                if rob_single_time_series!='undef' and rob_single_time_series >= 0 and j == len(time_series)-1:
                    rho.append(1)
                    
            #Satisfaction of a cell: 
            if rho[-1] > 0. :
                s = 1 
                break
            elif i == (r-1) and rho[-1] < 0.:
                s = -1
        
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        binary_tensor.append(parameters_min)
        # binary_tensor generic element is: parameters min, parameters max, s
        
    V = fun.Approx_Val( label, binary_tensor) 
    return V

def ExploreGridQuantitative( time_series , label,  grid , p_formula, sampling_freq, constant_definition):
    
    #The tensor is not binary here!
    tensor = []
    
    nb_parameters = len(grid.tensor)
    
    parameters_step = [list(np.arange(len(grid.tensor[par]))) for par in range(nb_parameters)]
    
    #number of valuations in each cell: r
    r = 99 #alpha = 0.05, p_0 = 0.03

    
    #Cartesian product of all combination of parameters
    #Describe each cell with a vector in [0,1]^ ( nb_parameters )
    for iprod_car in itertools.product(*parameters_step): # i.e., for each cell
        parameters_list = list(iprod_car)
        
        #Random uniform sampling 
        parameters_min = [ grid.tensor[par][parameters_list[par]][0] for par in range(nb_parameters)]
        parameters_max = [ grid.tensor[par][parameters_list[par]][1] for par in range(nb_parameters)]
        
        random_par = np.random.uniform(low=parameters_min, high=parameters_max, size=(r,nb_parameters))
        
        rho = []
        
        for i in range(r):
            parameters_valuation = random_par[i]
            
            parameters_valuation = fun.round_timing_parameters(parameters_valuation, sampling_freq, p_formula)
            
            rho_time_series = []
            
            for j, x in enumerate(time_series):
                formula = sr.instantiate_formula(p_formula, parameters_valuation)
                rob_single_time_series= sr.EvaluateRob(x,formula, sampling_freq, constant_definition)
                if rob_single_time_series!= 'undef': rho_time_series.append(rob_single_time_series)
            rho.append(min(rho_time_series))
            
        s = max(rho)
        
        
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        tensor.append(parameters_min)
        # binary_tensor generic element is: parameters min, parameters max, s
        
   
    V = fun.Approx_Val( label, tensor) 
            
    return V 

def ExploreGridMonotonic( time_series , label,  grid, mono , p_formula, sampling_freq, constant_definition):
    
    '''The function approximates the validity domain of the given times series with Fixed Granularity
    in case the parameteric specification is monotonic with respect to all its parameters.
    
    INPUT: - time_series, label,  grid as in the ExploreGrid function
           - mono: is a vector that specifies the kind of monotonicity for its parameters.
                   It has nb_parameters elements that can be 
                   either +1 if the monotonicity for that parameter is increasing
                   or -1 if the monotonicity for that parameter is decreasing.
    
    OUTPUT: - V = approximation of the validity domain (belonging to class Appox_Val)
           - W (if decomented) is used to compute a different overapproximation of the validity domain:
               
           Basically, a cell belongs to V if there exists at least one point 
           (that is the max in the monotonicity sense because for monotonicity reasons if one other point is satisfied, this is as well) 
           in the cell that is satisfied by ALL time series 
           (i.e., if the max point in the cell is not satisfied by at least one time series, the cell is not added to V)
           
           Conversely, a cell belongs to W if there exists at least one point in the cell
           which is satisfied by ONE time series 
           (i.e., if the max point in the cell is not satisfied by all time series, the cell is not added to V)
           
           V is then a subset of W
    
    '''
    
    binary_tensor = []
    # binary_tensor2 = []
    
    nb_parameters = len(grid.tensor)
    
    parameters_step = [list(np.arange(len(grid.tensor[par]))) for par in range(nb_parameters)]
    
    #number of valuations in each cell: r
    #r = 10
    
    #Cartesian product of all combination of parameters
    #Describe each cell with a vector in [0,1]^nb_parameters 
    for iprod_car in itertools.product(*parameters_step): # i.e., for each cell
        parameters_list = list(iprod_car)
        
        parameters_min = [ grid.tensor[par][parameters_list[par]][0] for par in range(nb_parameters)]
        parameters_max = [ grid.tensor[par][parameters_list[par]][1] for par in range(nb_parameters)]
        
        parameters_min_mon = [ ] #minimal point in the monotonicity sense: 
        # if it is satisfied, than the whole cell is satisfied (p if increasing, p+1 if decreasing)
        
        parameters_max_mon = [] #maximal point in the monotonicity sense: 
        # if it is not satisfied, than the whole cell is unsatisfied (p+1 if increasing, p if decreasing)
        
        ##Construction of the two quantities
        for par in range(nb_parameters):
            if mono[par] == 1:
                parameters_min_mon.append(parameters_min[par])
                parameters_max_mon.append(parameters_max[par])
                
            elif mono[par] == -1:
                parameters_min_mon.append(parameters_max[par])
                parameters_max_mon.append(parameters_min[par])
        
       
        parameters_max_mon = fun.round_timing_parameters(parameters_max_mon, sampling_freq, p_formula)
        
        boolean1 = False
        # boolean2 = False
        
        for i , x in enumerate(time_series):
            # Call tool rtamt to get robustness of trace x with respect to parameters paremeters_valuation
            formula = sr.instantiate_formula(p_formula, parameters_max_mon)
            rob_max = sr.EvaluateRob(x,formula, sampling_freq, constant_definition)
            
            if rob_max == 'undef' or rob_max < 0.: 
                s = -1 # if one time series do not satisfy --> the point is not part of the validity joint domain
                boolean1 = True
                # print(i ,max(x[3]), x[1],'dist_no_crash',  [(x[3][-2]**2)/(2*abs(x[4][-2]))], 'dist_crash',abs(x[2][-1]-x[-1][0] + 2.337 + 0.187),  parameters_max_mon)
                break
            
            # if rob_max != 'undef' and rob_max > 0.:
            #     s2 = 1
            #     boolean2 = True
            
            ##!!! 
            # if boolean1 == True and boolean2 == True: break
        
            if (i == len(time_series)-1): 
                if boolean1 == False: s = 1 #if ALL time series satisfy the point --> satisfaction of the whole cell
                # if boolean2 == False: s2 = -1
             
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        binary_tensor.append(parameters_min)
        # binary_tensor generic element is: parameters min, parameters max, s
        # if s==1: print(s)
        ###!!!
        # new_parameters_min = parameters_min.copy()
        # new_parameters_min[-1] = s2
        # binary_tensor2.append(new_parameters_min)
        
        
    V = fun.Approx_Val( label, binary_tensor) 
    # W = fun.Approx_Val( label, binary_tensor2)        
    return V#, W

