#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Search functions:
    - BinarySearch (binary satisfaction)
    - BinarySearchQuantitative (quantitative robustness)
    - AdaptGranularities (In case V1 and V2 have been approximated using BinarySearch, this method is necessary 
                          before applying ExtractParametersQuantitative.)
    - BinarySearchMonotonic (when monotonicity holds)
"""

import numpy as np
import itertools

import specs_rtamt as sr
import function as fun

def BinarySearch(time_series,  gran_min, par_bound, V , eval_par, p_formula, sampling_freq,  constant_definition):
    
    
    ''' The function computes the approximation of the validity domain of time series via binary search.
    
    Idea:
        
    A cell is considered: - if at least 80% of sampled parameter valuations in that cell satisfy: 
                                                    then the cell is associated with satisfaction;
                          - if at least 80% of sampled parameter valuations in that cell do not satisfy: 
                                                    then the cell is associated with non-satisfaction;
                          - otherwise the cell is splitted in 2^(nb_parameters) new cells
                                      and the algorithm is repeated on that new cells.
    Stopping criteria: minimal granularity reached.
    
    INPUT: - time series = set of time series associated with a single label
           - gran_min = list of minimal granularities on each parameter dimension.
           - par_bound = list of pairs [theta_min, theta_max] delimiting each 
                    parameter boundaries. The list has length number_parameters (number of parameters)
           - V = approximation of the validity domain computed so far
           - eval_par = parameters already evaluated in that cell ( one element is : [valuation_par1, val_par2, val_par3, s])
           - p_formula = parametric_formula
           - sampling_freq = list of two elements:
           
    OUTPUT: - V = approximation of the validity domain (belonging to class Appox_Val)
    
    N.B. : 
        
    eval_par : parameter evaluation already computed in previous steps and usable now
    
    new_possible_eval_par: parameter evaluation computed in this step + eval_par. 'Possible' referes 
                            to the fact that possibly are passed to a GENERIC cell in the next step in binary search  
                            (i.e. when s in neither more than 80% 1 nor more than 80% -1)
                            
    new__eval_par: subset of new_possible_eval_par that are passed to a PARTCILAR cell.
    
    '''
    ## PROCEDURE FOR ONE CELL
    
    nb_parameters = len(par_bound)
    
    parameters_min = [ par_bound[par][0] for par in range(nb_parameters)]
    parameters_max = [ par_bound[par][1] for par in range(nb_parameters)]

    
    #print(len(eval_par))
    ## !!! Check whether the parameters in eval_par are repeated in the sampled ones???
    number_sampled = 100 - len(eval_par) # number of parameters valuation to be evaluated in each cell
    
    ##RANDOM UNIFORM SAMPLING
    random_par = np.random.uniform(low=parameters_min, high=parameters_max, size=(number_sampled,nb_parameters))
    new_possible_eval_par = []
    
    #EVALUATION OF THE SATISFACTION OF THE r PARAMETERS VALUATION 
    rho = [] #List that will be long r and that represents the satisfaction 
    
    #Loop of NEW parameters valuation samples in a single cell
    for i in range(number_sampled): 
        parameters_valuation = random_par[i]
        
        parameters_valuation = fun.round_timing_parameters(parameters_valuation, sampling_freq, p_formula)
      
        new_possible_eval_par.append(list(parameters_valuation))
        
        #Loop to evaluate the satisfaction of a single parameter valuation
        for j, x in enumerate(time_series):
            # Call tool rtamt to get robustness of trace x with respect to parameters paremeters_valuation
            
            formula = sr.instantiate_formula(p_formula, parameters_valuation)
            rob_single_time_series = sr.EvaluateRob(x, formula, sampling_freq, constant_definition)
            
            
            # If ONE time-series does NOT satisfy, than the parameter valuation is associated with 0
            if rob_single_time_series == 'undef' or rob_single_time_series < 0.: 
                rho.append(-1)
                new_possible_eval_par[i].append(-1)
                break
            
            # If ALL time series satisfy, then the parameter valuation is associated with 1   
            if rob_single_time_series != 'undef' and rob_single_time_series >= 0. and j == len(time_series)-1:
                rho.append(1)
                new_possible_eval_par[i].append(1)
                
    # Adding the parameters valuations already computed
    for _ , e in enumerate(eval_par):
        new_possible_eval_par.append(e)
        rho.append(e[-1])
    
    #Satisfaction of a cell: 
    ## When more than 80% of random points have positive robustnesss
    ## rho is a list whose elements are either =1 or 1
    if len(np.where(np.array(rho) == 1.)[0]) >= ( (number_sampled+len(eval_par)) * 80/100):# and len(V.tensor)>=10: 
        s = 1 
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        V.tensor.append(parameters_min)
        # binary_tensor generic element is: parameters min, parameters max, s
        #print('a')
        return V
        
        
    
    ## When more than 80% of random points have negative robustnesss
    elif len(np.where(np.array(rho) == -1.)[0]) >= ( (number_sampled +len(eval_par) ) * 100/100) and len(V.tensor)>=10: 
        s = -1 
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        V.tensor.append(parameters_min)
        #print('b')
        return V
    
    else: 
        
        ##ALL minimal granularities have been reached: STOP!
        diff = np.array(parameters_max) - np.array(parameters_min) 
        if max(diff - np.array(gran_min))<= 1e-6: # if granularity reached (1e-6 to avoid problems with numerical values)
           
            # if len(np.where(np.array(rho) > 0.)[0]) >= (number_sampled+len(eval_par))/2 : s = 1 
            # else: s = 0 
            
            if (max(rho) > 0): s = 1 
            else: s = 0 
            
            
            parameters_max.append(s)
            parameters_min.extend(parameters_max)
            V.tensor.append(parameters_min)
            #print('c')
            return V
        
        
        ## Need to split again --> RECURSIVE STEP
        else: 
            #print('d')
            # Need q this to enumerate partition of the cell
            q = [] # q = [ [0,1] , [0,1], ... , [0,1]]
            for i in range(nb_parameters):
                q.append([0,1])
                
            # Loop long 2^(#number of parameters):    
            for iprod_car in itertools.product(*q): # for every combination of parameters
                new_par_bound = []
                new_eval_par = []
                
                # Definition of new parameters bound
                for i in range(nb_parameters): 
                    # For every parameter decide whether to take the original or the mid point 
                    if iprod_car[i]==0: coordinate = [par_bound[i][0], (par_bound[i][0]+par_bound[i][1])/2 ]
                    elif iprod_car[i]==1: coordinate = [ (par_bound[i][0]+par_bound[i][1])/2 , par_bound[i][1] ]
                    new_par_bound.append(coordinate) 
                    
                
                # Definition of parameters valuations already computed that belong to the new cell
                for i , npep in enumerate(new_possible_eval_par):
                    
                    for j in range(len(npep)-1):
                        if npep[j]<new_par_bound[j][0] or npep[j] > new_par_bound[j][1]: break
                        if j == len(npep)-2: new_eval_par.append(npep)
                        
                # Removing parameters valuation that have been used already in the current cell
                for _ , nep in enumerate(new_eval_par):  new_possible_eval_par.remove(nep)
                        
                # The changes in the inputs are --> parameters_bounds : it delimites the new cell
                #                               --> eval_par : parameters already eveluated        
                
                V = BinarySearch(time_series,  gran_min, new_par_bound,  V , new_eval_par , p_formula, sampling_freq,  constant_definition) 
    return V


def BinarySearchMonotonic(time_series,  gran_min, par_bound, V ,eval_par,  mono,  p_formula, sampling_freq, constant_definition, counter):
    
    '''The function approximates the validity domain of the given times series with BinarySearch
    in case the parameteric specification is monotonic with respect to all its parameters.
    
    INPUT: - time_series, gran_min, par_bound , V as in the BinarySearch function
           - mono: is a vector that specifies the kind of monotonicity for its parameters.
                   It has nb_parameters elements that can be 
                   either +1 if the monotonicity for that parameter is increasing
                   or -1 if the monotonicity for that parameter is decreasing.
           - p_formula: parametric formula
           - sampling_freq = list of two elements 
           
    
    OUTPUT: - V = approximation of the validity domain (belonging to class Appox_Val)
    '''
    
    ## PROCEDURE FOR ONE CELL
    nb_parameters = len(par_bound)
    
    number_sampled = 100 - len(eval_par) # number of parameters valuation to be evaluated in each cell
    
    
    # Parameters minimal and maximal of each parameter dimension. 
    # They define the bounds of the cell in each dimension
    parameters_min = [ par_bound[par][0] for par in range(nb_parameters)]
    parameters_max = [ par_bound[par][1] for par in range(nb_parameters)]
    
    #The two quantities depend on the monotonicity sign
    parameters_min_mon = [ ] #minimal point in the monotonicity sense: 
    # if it is satisfied, than the whole cell is satisfied (p if increasing, p+1 if decreasing)
    min_already_evaluated = False
    
    parameters_max_mon = [] #maximal point in the monotonicity sense: 
    # if it is not satisfied, than the whole cell is unsatisfied (p+1 if increasing, p if decreasing)
    max_already_evaluated = False
    
    new_possible_eval_par = []
    
    
    
    ##Construction of the two quantities
    for par in range(nb_parameters):
        if mono[par] == 1:
            parameters_min_mon.append(parameters_min[par])
            parameters_max_mon.append(parameters_max[par])
            
        elif mono[par] == -1:
            parameters_min_mon.append(parameters_max[par])
            parameters_max_mon.append(parameters_min[par])
    
    
    parameters_max_mon = fun.round_timing_parameters(parameters_max_mon, sampling_freq, p_formula)
    parameters_min_mon = fun.round_timing_parameters(parameters_min_mon, sampling_freq, p_formula)
   
    ## Check whether HIGHEST and/or LOWEST points have already been evaluated:
       
    for index , el in enumerate(eval_par):
        
        if el[:-1] == parameters_max_mon: max_already_evaluated = el[-1]
        
        elif el[: -1 ] == parameters_min_mon: min_already_evaluated = el[-1]
        
        #Both have been
        if max_already_evaluated != False and min_already_evaluated != False : break
   
    
    evaluation = 'start' 
    
    if max_already_evaluated == False:
    
        new_possible_eval_par.append(parameters_max_mon)
        formula = sr.instantiate_formula(p_formula, parameters_max_mon)
        
        ## Evaluation of the HIGHEST point : if violated ->  all cell is violated
        counter += 1
        for i , x in enumerate(time_series):
            
            rob_max = sr.EvaluateRob(x, formula, sampling_freq, constant_definition)
            
            # If ONE time-series does NOT satisfy parameters_max_mon then the whole cell is not satisfied
            if rob_max == 'undef' or rob_max < 0.: 
                    evaluation = 'unsat'
                    new_possible_eval_par[-1].append(-1)
                    break
                
    elif  max_already_evaluated < 0.: evaluation = 'unsat'
      
    
    if evaluation != 'unsat':
        
        if max_already_evaluated == False: new_possible_eval_par[-1].append(1) #the parameters_max_mon is satisfied
        
        if min_already_evaluated == False:
        
            new_possible_eval_par.append(parameters_min_mon)
            
            ## Evaluation of the LOWEST point : if satisfied ->  all cell is satisfied
            formula = sr.instantiate_formula(p_formula, parameters_min_mon)
            
            counter += 1
            for i , x in enumerate(time_series):
                rob_min = sr.EvaluateRob(x,formula, sampling_freq, constant_definition)
                
                if rob_min == 'undef' or (rob_min!= 'undef' and rob_min < 0.):
                    evaluation = 'unknown'
                    new_possible_eval_par[-1].append(-1)
                    break
                    # If ALL time series satisfy parameters_min_mon then the whole cell is satisfied 
                if (i == len(time_series)-1) and (evaluation != 'unknown') : 
                    evaluation = 'sat'
                    new_possible_eval_par[-1].append(1)
                    
        elif min_already_evaluated < 0.: evaluation = 'unknown'
        elif min_already_evaluated > 0. : evaluation = 'sat'
    
        
    # min_length = 0
    if evaluation == 'sat': #  and len(V.tensor)>= min_length: 
        s = 1 
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        V.tensor.append(parameters_min)
        #print('sat')
        return V, counter
        
    elif evaluation == 'unsat': #  and len(V.tensor)>= min_length:
        s = -1 
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        V.tensor.append(parameters_min)
        #print('unsat')
        return V, counter
        
    elif evaluation == 'unknown': # or len(V.tensor)< min_length: 
        
        diff = np.array(parameters_max) - np.array(parameters_min) 
        
        #Minimal granularities has already been reached
        if max(diff - np.array(gran_min))<= 1e-6: # if granularity reached (1e-6 to avoid problems with numerical values)
            
            ##RANDOM UNIFORM SAMPLING
            random_par = np.random.uniform(low=parameters_min, high=parameters_max, size=(number_sampled,nb_parameters))
            rho = [] #List that will be long random_par and that represents the satisfaction 
            
            bool_eval = True
            
            
            # Adding the parameters valuations already computed
            for _ , e in enumerate(eval_par):
                new_possible_eval_par.append(e)
                rho.append(e[-1])
                
                if rho[-1] > 0. :
                    s = 1 
                    bool_eval = False
                    break
                
            
            if bool_eval :
                #Loop of parameters valuation samples in a single cell
                for i in range(number_sampled): 
                    parameters_valuation = random_par[i]
                    parameters_valuation = fun.round_timing_parameters(parameters_valuation, sampling_freq, p_formula)
        
                    new_possible_eval_par.append(list(parameters_valuation))
                    
                    #Loop to evaluate the satisfaction of a single parameter valuation
                    for j, x in enumerate(time_series):
                        # Call tool rtamt to get robustness of trace x with respect to parameters paremeters_valuation
                        formula = sr.instantiate_formula(p_formula, parameters_valuation)
                        rob_single_time_series = sr.EvaluateRob(x, formula , sampling_freq, constant_definition)
                        
                        # If ONE time-series does NOT satisfy, than the parameter valuation is associated with 0
                        if rob_single_time_series == 'undef' or rob_single_time_series < 0.: 
                            rho.append(-1)
                            new_possible_eval_par[-1].append(-1)
                            break
                        
                        # If ALL time series satisfy, then the parameter valuation is associated with 1   
                        if rob_single_time_series != 'undef' and rob_single_time_series >= 0. and j == len(time_series)-1: 
                            rho.append(1)
                            new_possible_eval_par[-1].append(1)
                    
                    #Satisfaction of a cell: if at least one satisfied parameter valuation has been found
                    if rho[-1] > 0. :
                        s = 1 
                        break
                    
                    elif i == (number_sampled -1) and rho[-1] < 0.:
                        s = -1
               
            parameters_max.append(s)
            parameters_min.extend(parameters_max)
            V.tensor.append(parameters_min)
        
            return V, counter
            
        #Minimal granularity has not been reached, so the cell is split. 
        # RECURSIVE STEP
        else:
            #print('d')
            # Need q this to enumerate partition of the cell
            q = [] # q = [ [0,1] , [0,1], ... , [0,1]]
            for i in range(nb_parameters):
                q.append([0,1])
                
            # Loop long 2^(#number of parameters):    
            for iprod_car in itertools.product(*q): # for every combination of parameters
                new_par_bound = []
                new_eval_par = []
                
                # Definition of new parameters bound
                for i in range(nb_parameters): 
                    # For every parameter decide whether to take the original or the mid point 
                    if iprod_car[i]==0: coordinate = [par_bound[i][0], (par_bound[i][0]+par_bound[i][1])/2 ]
                    elif iprod_car[i]==1: coordinate = [ (par_bound[i][0]+par_bound[i][1])/2 , par_bound[i][1] ]
                    new_par_bound.append(coordinate) 
                
                # Definition of parameters valuations already computed that belong to the new cell
                for i , npep in enumerate(new_possible_eval_par):
                    
                    for j in range(len(npep)-1):
                        if npep[j]<new_par_bound[j][0] or npep[j] > new_par_bound[j][1]: break
                        if j == len(npep)-2: new_eval_par.append(npep)
                        
                # Removing parameters valuation that have been used already in the current cell
                for _ , nep in enumerate(new_eval_par):  new_possible_eval_par.remove(nep)
                        
                # The changes in the inputs are --> parameters_bounds : it delimites the new cell
                #                               --> eval_par : parameters already eveluated        
                
                V, counter = BinarySearchMonotonic(time_series,  gran_min, new_par_bound,  V ,new_eval_par , mono , p_formula, sampling_freq, constant_definition, counter) 
    
    else: print('Error!')
            
    return V, counter



def BinarySearchQuantitative(time_series,  gran_min, par_bound, V , eval_par, p_formula, sampling_freq, constant_definition):
    
    ## PROCEDURE FOR ONE CELL
    
    nb_parameters = len(par_bound)
    
    parameters_min = [ par_bound[par][0] for par in range(nb_parameters)]
    parameters_max = [ par_bound[par][1] for par in range(nb_parameters)]

    
    #print(len(eval_par))
    ## !!! Check whether the parameters in eval_par are repeated in the sampled ones???
    number_sampled = 100 - len(eval_par) # number of parameters valuation to be evaluated in each cell
    
    ##RANDOM UNIFORM SAMPLING
    random_par = np.random.uniform(low=parameters_min, high=parameters_max, size=(number_sampled,nb_parameters))
    new_possible_eval_par = []
    
    #EVALUATION OF THE SATISFACTION OF THE r PARAMETERS VALUATION 
    rho = [] #List that will be long r and that represents the satisfaction 
    
    #Loop of NEW parameters valuation samples in a single cell
    for i in range(number_sampled): 
        
        parameters_valuation = random_par[i]
        
        parameters_valuation = fun.round_timing_parameters(parameters_valuation, sampling_freq, p_formula)
    
        new_possible_eval_par.append(list(parameters_valuation))
        
        rho_time_series = [] #Stores the robustness of different time series on the same parameter valuation
            
        #Loop to evaluate the satisfaction of a single parameter valuation
        for j, x in enumerate(time_series):
            # Call tool rtamt to get robustness of trace x with respect to parameters paremeters_valuation
            formula = sr.instantiate_formula(p_formula,parameters_valuation)
            rob_single_time_series = sr.EvaluateRob(x, formula, sampling_freq, constant_definition )
            if rob_single_time_series!= 'undef': rho_time_series.append(rob_single_time_series)
            
        rho.append(np.mean(rho_time_series))
        new_possible_eval_par[i].append(np.mean(rho_time_series))
                
    # Adding the parameters valuations already computed
    for _ , e in enumerate(eval_par):
        new_possible_eval_par.append(e)
        rho.append(e[-1])
    
    #print(rho, len(rho))
    ## rho is a list whose elements are the robustness values of the parameter valuations
    
    #Satisfaction of a cell: 
    ## When more than 80% of random points have positive robustnesss
    if len(np.where(np.array(rho) >0.)[0]) >= ( (number_sampled+len(eval_par)) * 80/100) and len(V.tensor)>=10: 
        s = np.mean(rho)
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        V.tensor.append(parameters_min)
        # tensor generic element is: parameters min, parameters max, s
        #print('a')
        return V
        
    ## When more than 80% of random points have negative robustnesss
    elif len(np.where(np.array(rho) <0.)[0]) >= ( (number_sampled +len(eval_par) ) * 100/100) and len(V.tensor)>=10: 
        s = np.mean(rho) 
        #Append the parameters defining the cell and its satisfaction value
        parameters_max.append(s)
        parameters_min.extend(parameters_max)
        V.tensor.append(parameters_min)
        #print('b')
        return V
    
    else: 
        
        ## ALL minimal granularities have been reached: STOP!
        diff = np.array(parameters_max) - np.array(parameters_min) 
        
        if max(diff - np.array(gran_min))<= 1e-6: # if granularity reached (1e-6 to avoid problems with numerical values)
            
            ## ??? s=0 or take the mean anyway?
            s = 0 # grey cell
            
            parameters_max.append(s)
            parameters_min.extend(parameters_max)
            V.tensor.append(parameters_min)
            #print('c')
            return V
        
        ## Need to split again --> RECURSIVE STEP
        else: 
            #print('d')
            # Need q this to enumerate partition of the cell
            q = [] # q = [ [0,1] , [0,1], ... , [0,1]]
            for i in range(nb_parameters):
                q.append([0,1])
                
            # Loop long 2^(#number of parameters):    
            for iprod_car in itertools.product(*q): # for every combination of parameters
                new_par_bound = []
                new_eval_par = []
                
                # Definition of new parameters bound
                for i in range(nb_parameters): 
                    # For every parameter decide whether to take the original or the mid point 
                    if iprod_car[i]==0: coordinate = [par_bound[i][0], (par_bound[i][0]+par_bound[i][1])/2 ]
                    elif iprod_car[i]==1: coordinate = [ (par_bound[i][0]+par_bound[i][1])/2 , par_bound[i][1] ]
                    new_par_bound.append(coordinate) 
                    
                
                # Definition of parameters valuations already computed that belong to the new cell
                for i , npep in enumerate(new_possible_eval_par):
                    
                    for j in range(len(npep)-1):
                        if npep[j]<new_par_bound[j][0] or npep[j] > new_par_bound[j][1]: break
                        if j == len(npep)-2: new_eval_par.append(npep)
                        
                # Removing parameters valuation that have been used already in the current cell
                for _ , nep in enumerate(new_eval_par):  new_possible_eval_par.remove(nep)
                        
                # The changes in the inputs are --> parameters_bounds : it delimites the new cell
                #                               --> eval_par : parameters already eveluated        
                
                V = BinarySearchQuantitative(time_series,  gran_min, new_par_bound,  V , new_eval_par,  p_formula, sampling_freq,  constant_definition) 
          
    return V

def AdaptGranularities(V1, V2, label2):
    
    ## Hyphotesis: Every split (in BinarySearch) implies a split in all the dimensions 
    ''' The fuction adapt V1 and V2 to have the same cells. 
    In case V1 and V2 have been approximated using BinarySearch, this method is necessary 
    before applying ExtractParametersQuantitative. '''
    
    nb_parameters = (len(V1.tensor[0])-1)//2
    
    ## Indices of cells that are big, in the sense that in the validity domain of the other class it has ben split
    V1_to_be_deleted = [] # indices of elements to be deleted from V1.tensor
    V2_to_be_deleted = [] # indices of elements to be deleted from V2.tensor
    
    ##New cells that will replace the 'big' ones. 
    ## The robustness value will be the same as the original cell they coome from
    V1_to_be_added = [] # list of elements (of length (2*nb_paremeters + 1)) to be added to V1
    V2_to_be_added = [] # list of elements (of length (2*nb_paremeters + 1)) to be added to V2
  
    
    for indx1, element1 in enumerate(V1.tensor):
        for indx2, element2 in enumerate(V2.tensor):
            
            ## Assuming that every split (in BinarySearch) implies a split in all the dimensions  
            ## For this reason the 'PROPER' inclusion between cells in different validity domain 
            ##is checked ONLY IN THE FIRST DIMENSION
            
            
            # If cell in V1 is included in V2
            if  (element2[0] <=         element1[0]         <= element2[0 + nb_parameters]) and \
                (element2[0] <= element1[0 + nb_parameters] <= element2[0 + nb_parameters]) and \
                (element1[0] != element2[0] or element1[nb_parameters] != element2[nb_parameters]):
                        for par in range(1, nb_parameters): #Need to check all the dimensions are included
                            if not((element2[par] <= element1[par]<= element2[par + nb_parameters]) \
                                    and(element2[par] <= element1[par + nb_parameters]<= element2[par + nb_parameters])) :
                                  stop = True # If one parameter dimension then no inclusion between cells is present
                                  break
                            stop = False
                        if stop == False:
                            V2_to_be_deleted.append(indx2)
                            ## The new cell in V2 will have paremeters dimensions of the small cell in V1 
                            ## and robustness value of the original big cell in V2 (of which the new cell is a part)
                            V2_to_be_added.append( element1[:-1] + [element2[-1]]) 
  
            
            # If cell in V2 is included in V1    
            elif (element1[0] <=         element2[0]         <= element1[0 + nb_parameters]) and \
                  (element1[0] <= element2[0 + nb_parameters] <= element1[0 + nb_parameters]) and \
                  (element2[0] != element1[0] or element2[nb_parameters] != element1[nb_parameters]):
                        for par in range(1, nb_parameters):
                            if not((element1[par] <= element2[par]<= element1[par + nb_parameters]) \
                                    and(element1[par] <= element2[par + nb_parameters]<= element1[par + nb_parameters])): 
                                stop = True
                                break
                            stop = False
                        if stop == False:
                            V1_to_be_deleted.append(indx1)
                            ## The new cell in V1 will have paremeters dimensions of the small cell in V2 
                            ## and robustness value od the old big cell in V1
                            V1_to_be_added.append( element2[:-1] + [element1[-1]]) 
                        
    
    ## Remove 'big' cells from V1 (i.e., cells that include entire cells in V2)
    V1_to_be_deleted = sorted(list(set(V1_to_be_deleted)) , reverse = True) #list_set is used to eliminate duplicates
    for idx in V1_to_be_deleted:
        if idx < len(V1.tensor):
            V1.tensor.pop(idx)
    
    ## Add small new cells to V1
    for element in V1_to_be_added:
        V1.tensor.append(element)
      
    ## Remove 'big' cells from V2 (i.e., cells that include entire cells in V1)
    V2_to_be_deleted = sorted(list(set(V2_to_be_deleted)) , reverse = True) #list_set is used to eliminate duplicates
    for idx in V2_to_be_deleted:
        if idx < len(V2.tensor):
            V2.tensor.pop(idx)
           
    ## Add small new cells to V2
    for element in V2_to_be_added:
        V2.tensor.append(element)
        
    ## CELLS ORDERING    
    ## The order of cells in V1 is manteined. The order in V2 is changed to be the same as V1.
    new_tensor = []
    for _, element1 in enumerate(V1.tensor):
        for _, element2 in enumerate(V2.tensor):
            if element1[:-1] == element2[:-1]:
                new_tensor.append(element2)
                break
    
    V2 = fun.Approx_Val(label2, new_tensor)
    
    return V1, V2


