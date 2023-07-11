#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import itertools

import scipy
from scipy import spatial
# import pandas as pd


class Approx_Val:
    
    '''Approximation of the Validity Domain of (PSTL formula, time series belonging to the same class).
    
       The features are:
           label = class 
           tensor =  tensor representing parameteres valuations and 0-1 satisfaction.
    '''
    
    def __init__(self,   label, tensor ):
                    
        self.label = label
        self.tensor = tensor 
        return
   
    
 
## Grid.tensor has a differtent strcuture of Approx_Val.tensor. They are 2 different thinghs!!!
class Grid:
    
    ''' Grid of the parameters space of the PSTL formula with respect to the given granularity.
    
        Features are:
            
            par_bound = parameter space: list of pairs [theta_min, theta_max] delimiting each 
                parameter boundaries
            gran = vector of granularities (granularity on each dimension)
            tensor = grid in a tensor structure. See OUTPUT in CreateGrid function
        
    '''
    
    def __init__(self,  par_bound, gran, tensor):

        self.par_bound = par_bound
        self.gran = gran
        self.tensor = tensor
        
        return
    

    
def CreateGrid(par_bound, gran):
    
    ''' The function computes the approximation of the parameter space associated 
        to the PSTL template in a grid, given the desired granularity and the maximum 
        and minimum values allowed for each parameter.
    
        INPUT:
            - par_bound = list of pairs [theta_min, theta_max] delimiting each 
                    parameter boundaries. The list has length number_parameters (number of parameters)
            - gran = list of granularities on each parameter dimension. 
                   The list has length number_parameters (number of parameters)
                   
        OUTPUT:
            - tensor of dimensions: [theta_max - theta_min]/gran on each dimension. Number 
                of dimension is number_parameters
                Represented as a list:
                    first dimension: selection of parameter  
                    second dimnesion: parameter space partition 
                    (ex. tensor = [ - , -, -, -, .., -] . each - is a dimension
                        tensor[0]= whole partition of parameter 0, that is tensor[0] = [ [-,-] , [-,-] , ... , [-,-]],
                        it has lenght number_steps and 
                        tensor[0][0]= [theta_min, theta_min + gran] : elements defining the partition)
            
    '''
    
    number_parameters = len(par_bound)
    tensor = []
    
    for par in range(number_parameters):
        partition = []
        
        # Number of steps has to be an integer. Using // in the division makes it an integer,
        # but starting from thata_min and moving of quantity gran for number_steps , we get a number
        # generally <= theta_max. If we do not want to have <, then consider adding +1 to number of steps
        
        number_steps = int((par_bound[par][1] - par_bound[par][0]) // gran[par])  ## (theta_max - theta_min)/gran
        start = par_bound[par][0] # theta_min
        
        for i in range(number_steps):  
            partition.append([start, start + gran[par]])
            start += gran[par]
        
        tensor.append(partition)
        
        
    grid = Grid( par_bound, gran, tensor)
    
    return grid

def round_timing_parameters(old_param, sampling_freq, p_formula):       
 
     # if type(old_param) == float: new_param = [old_param]
     # else: new_param = old_param.copy()
     new_param = old_param.copy()
     
     #Do not round if non-integer numbers are accepted as time values
     if type(sampling_freq[0]) != int: return new_param
     
     for i in range(20): #max 20 parameters
         #If timing parameter
         if f'[epsilon{i}-' in p_formula or f'epsilon{i}-]' in p_formula or \
            f'[ epsilon{i}-'in p_formula or f'epsilon{i}- ]' in p_formula: 
            new_param[i] = round(old_param[i]) 

             
     return new_param
 

    
def ExtractParameters(V1, V2, sed):
    
    '''The function chooses a parameter valuation for each of the two classes (inside the respective approximated-validity domain),
        such that the distance between the two points corresponds to the Hausdorff distance between the two sets (validity domains).
    
    INPUT:
        - V1: approximation of the validity domain for the first class
        - V2: approximation of the validity domain for the second class
        
    OUTPUT:   
        
        - parameters: 2 elements.
          The first element corresponds to the parameter to be used for the first class,
          The second  for parameters that characterize the second class.
    
    '''
    
    #nb_dimensions = 2*nb_parameters(Each parameter has the minimum and maximum value)
    nb_dimensions = len(V1.tensor[0]) - 1 
    nb_parameters = int(nb_dimensions/2)
    
    # It will be used to enumerate all extreme points of a cell
    q = []
    for i in range(nb_parameters):
        q.append([0,1])
        
    
    ## Collect set of points in class 1 having positive satisfaction value
    
    X1 = []
  
    #One for each cell in the parameter space
    for cell in range(len(V1.tensor)): 
        
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        #if V1.tensor[cell][-1] > 0.:
        ###!!! Added for the case in which a part of the parameter space is not a number but instead is 'undef'
        if ( V1.tensor[cell][-1] != 'undef') and float(V1.tensor[cell][-1]) > 0.:
            
            # Append all the extreme points of the cell.
            # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V1.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V1.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    # print(extreme_point)
                    X1.append( extreme_point ) #parameters valuation without satisfaction vector
                # print(len(X1))
                # CalculateContour(V1.tensor[cell][:-1], X1)
                # print(len(X1))  
                    
    ## Collect set of points in class 2 having positive satisfaction value
    X2 = []
  
    #One for each cell in the parameter space
    for cell in range(len(V2.tensor)): 
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        # if V2.tensor[cell][-1] > 0.:
        ###!!! Added the the case in which a part of the parameter space is not a number but instead is 'undef'
        if (V2.tensor[cell][-1] != 'undef') and float(V2.tensor[cell][-1]) > 0.:    
            # Append all the extreme points of the cell.
            # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V2.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V2.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    
                    X2.append( extreme_point ) #parameters valuation without satisfaction vector
                # CalculateContour(V2.tensor[cell][:-1],X2)
                    
    if len(X1) == 0 or len(X2)==0:
        print('At least one Validity domain is empty !!!')
        return 
    
    ### !!!
    # if spec == 0: parameters = [ find_max_min(X1), find_max_min(X2)]

    # else:
    
    # Take the point in X1 that is the farest from X2 --> X1[index_1A]
    d1, index_1A , _  = scipy.spatial.distance.directed_hausdorff(X1, X2, seed=sed)

    # Take the point in X2 that is the farest from X1 --> X2[index_2A]
    d2, index_2B,  _  = scipy.spatial.distance.directed_hausdorff(X2, X1, seed=sed)
    ## The Hausdorff distance would be the maximum between the two directed 'distances'
    # print(d1, d2)

    parameters = [ X1[index_1A], X2[index_2B]  ]
    
    return parameters


def ExtractParameters_DOMAIN_KNOWLEDGE(V1, V2):
    
    #nb_dimensions = 2*nb_parameters(Each parameter has the minimum and maximum value)
    nb_dimensions = len(V1.tensor[0]) - 1 
    nb_parameters = int(nb_dimensions/2)
    
    # It will be used to enumerate all extreme points of a cell
    q = []
    for i in range(nb_parameters):
        q.append([0,1])
        
    ## Collect set of points in class 1 having positive satisfaction value
    X1 = []
  
    #One for each cell in the parameter space
    for cell in range(len(V1.tensor)): 
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        #if V1.tensor[cell][-1] > 0.:
        ###!!! Added for the case in which a part of the parameter space is not a number but instead is 'undef'
        if ( V1.tensor[cell][-1] != 'undef') and float(V1.tensor[cell][-1]) > 0.:
            
            # Append all the extreme points of the cell.
            # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V1.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V1.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    # print(extreme_point)
                    X1.append( extreme_point ) #parameters valuation without satisfaction vector
                # print(len(X1))
                # CalculateContour(V1.tensor[cell][:-1], X1)
                # print(len(X1))  
                    
    ## Collect set of points in class 2 having positive satisfaction value
    X2 = []
  
    #One for each cell in the parameter space
    for cell in range(len(V2.tensor)): 
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        # if V2.tensor[cell][-1] > 0.:
        ###!!! Added the the case in which a part of the parameter space is not a number but instead is 'undef'
        if (V2.tensor[cell][-1] != 'undef') and float(V2.tensor[cell][-1]) > 0.:    
            # Append all the extreme points of the cell.
            # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V2.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V2.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    
                    X2.append( extreme_point ) #parameters valuation without satisfaction vector
                # CalculateContour(V2.tensor[cell][:-1],X2)
                    
    if len(X1) == 0 or len(X2)==0:
        print('At least one Validity domain is empty !!!')
        return 
    
  
    parameters = [ find_max_min(X1), find_max_min(X2)]
    
    return parameters



def find_max_min(set_points):
    
    aux = set_points[0].copy()
    for i in range(1, len(set_points)):
        if set_points[i][0] > aux[0]: aux = set_points[i].copy()
        elif set_points[i][0] == aux[0]:
            if set_points[i][1] < aux[1]: aux = set_points[i].copy()
    return aux
            
        

def ExtractParametersMultiple(V1, V2, V3, sed, bool_mono, mono): #V1 vs(V2 union V3)
    
    #nb_dimensions = 2*nb_parameters(Each parameter has the minimum and maximum value)
    nb_dimensions = len(V1.tensor[0]) - 1 
    nb_parameters = int(nb_dimensions/2)
    
    # It will be used to enumerate all extreme points of a cell
    q = []
    for i in range(nb_parameters): q.append([0,1])
        
    ## Collect set of points in class 1 having positive satisfaction value
    X1 = []
  
    #One for each cell in the parameter space
    for cell in range(len(V1.tensor)): 
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        if V1.tensor[cell][-1]!= 'undef' and V1.tensor[cell][-1] > 0.:# and V2.tensor[cell][-1]>0 :
            
            if bool_mono:
                parameters_min = V1.tensor[cell][0:nb_parameters]
                parameters_max = V1.tensor[cell][nb_parameters: 2*nb_parameters]
                
                parameters_max_mon = [] #maximal point in the monotonicity sense: 
                for par in range(nb_parameters):
                    if mono[par] == 1: parameters_max_mon.append(parameters_max[par])
                    elif mono[par] == -1: parameters_max_mon.append(parameters_min[par])
                    
                X1.append(parameters_max_mon)    
          
            else:
                # Append all the extreme points of the cell.
                # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V1.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V1.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    
                    if extreme_point[1]<extreme_point[2]:X1.append( extreme_point ) #parameters valuation without satisfaction vector
                CalculateContour(V1.tensor[cell][:-1], X1)
                    
                    
    ## Collect set of points in class 2 having positive satisfaction value
    X2 = []
  
    # One for each cell in the parameter space
    for cell in range(len(V2.tensor)): 
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        if V2.tensor[cell][-1]!= 'undef' and V2.tensor[cell][-1] > 0.:
            
            
            # Append all the extreme points of the cell.
            # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V2.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V2.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    
                    if extreme_point[1]<extreme_point[2]:X2.append( extreme_point ) #parameters valuation without satisfaction vector
                
                CalculateContour(V2.tensor[cell][:-1],X2)
                
                
    for cell in range(len(V3.tensor)): 
        
        # if the parameter valuation in cell is 1 (i.e., class satisfies phi with parameters in cell)
        if V3.tensor[cell][-1]!= 'undef' and V3.tensor[cell][-1] > 0.:
            
            # Append all the extreme points of the cell.
            # The number of extreme points is 2^(number of parameteres).
                for iprod_car in itertools.product(*q):
                    extreme_point = []
                    
                    for i in range(nb_parameters):
                        if iprod_car[i]==0: coordinate = V3.tensor[cell][i]
                        elif iprod_car[i]==1: coordinate = V3.tensor[cell][i + nb_parameters]
                        extreme_point.append(coordinate)
                    
                    if extreme_point[1]<extreme_point[2]:X2.append( extreme_point ) #parameters valuation without satisfaction vector
                CalculateContour(V3.tensor[cell][:-1],X2)
    if len(X1) == 0 or len(X2)==0:
        print('At least one Validity domain is empty !!!')
        return 
    
  
    # Take the point in X1 that is the farest from X2 --> X1[index_1A]
    dist, index_1A , _  = scipy.spatial.distance.directed_hausdorff(X1, X2, seed= sed)
    
    print('dist=', dist)
    parameters = [ X1[index_1A] ]
    return parameters


def CalculateContour(cell_bound, X):
    
    '''Given the 2^n extreme points of a cell, the function computes points in the (n-1)
    dimensional space in order to evaluate the Haudorff distance.
    If , for example, n=2, given the 4 extremes of a square the function samples points in its contour.'''
    
    number_sampled = 200
    nb_parameters = len(cell_bound)//2
    
    parameters_min = [ cell_bound[par] for par in range(nb_parameters)]
    parameters_max = [ cell_bound[par + nb_parameters] for par in range(nb_parameters)]

    
    # Loop over the minimal parameter dimension
    for par in range(len(cell_bound)):
        
        #Removing from list parameters_min the value relative to the parameter dimension 'par'
        parameters_min_sampling = parameters_min.copy()
        if par < nb_parameters: parameters_min_sampling.pop(par)
        else: parameters_min_sampling.pop(par - nb_parameters)
        
        #Removing from list parameters_max the value relative to the parameter dimension 'par'
        parameters_max_sampling = parameters_max.copy()
        if par < nb_parameters: parameters_max_sampling.pop(par)
        else: parameters_max_sampling.pop(par - nb_parameters)
        
        # Sampling number_sampled 
        random_par = np.random.uniform(low=parameters_min_sampling, high=parameters_max_sampling, size=(number_sampled,nb_parameters - 1))
        
        ## For each sample the parameter valued relative to dimension par are reinserted
        for j in range(number_sampled):
            
            random_sample = list(random_par[j])
            if par < nb_parameters: random_sample.insert(par, cell_bound[par])
            else: random_sample.insert(par - nb_parameters , cell_bound[par])
            #if random_sample[1]< random_sample[2]: 
            X.append(random_sample)
    return


def ExtractParametersQuantitative(V1, V2): #, V3):
    
    '''  The function chooses a point with POSITIVE ROBUSTNESS for V1 such that it maximizes the absolute 
        value of the difference with the robustness of the corresponding point in V2.
        First the search is done among points that in V2 that have NEGATIVE ROBUSTNESS. If no such points
        exist (a point with positive rob in V1 and negative rob in V2, i.e. if V1 is a subset of V2),
        then the search is done among any point in V2. 
        
        N.B.
        The same partition of the parameters space is supposed for V1 and V2. 
        
        AND THE SAME ORDER!!!
        
        (This is always true when V1 and V2 came from the approximation with a fixed granularity.)
        If BinarySearch has been used, apply first the function AdaptGranularities.
    '''
    
    s1 = [] # s1 = vector of robustness values for V1
    for index_1 in range(len(V1.tensor)): 
        if V1.tensor[index_1][-1]!= 'undef': #float(V1.tensor[index_2][1])< float(V1.tensor[index_2][2]):
            s1.append(float(V1.tensor[index_1][-1]) )
        else: s1.append(-1)
            
    s1 = np.array(s1)
    rob1 = np.where(s1 > 0)[0] #indices where V1 has positive robustness
    
    s2 = [] #s2 = vector of robustness values for V2
    for index_2 in range(len(V2.tensor)):  
        if V1.tensor[index_1][-1]!= 'undef':
            'When computing wrt 3 tensors'
            s2.append(float(V2.tensor[index_2][-1]))  #( max(V2.tensor[index_2][-1], V3.tensor[index_2][-1])) # 
        else: 
            s2.append(1)
    s2 = np.array(s2)
    rob2 = np.where(s2 < 0)[0] #indices where V2 has negative robustness
    
    intersection = list(set(rob1).intersection(rob2)) # indices of the intersection between rob1 and rob 2
    
    if len(intersection) > 0: # search among points with rob(V1) >=0 and rob(V2)<=0
        best_cell_index = intersection[np.argmax(( s1[intersection]-s2[intersection]))]  
        print(s1[best_cell_index] - s2[best_cell_index])
        print(':)' )
    elif len(rob1)> 0: # otherwise, no restriction from V2, but the point has to be in rob(V1)>=0 anyway
        best_cell_index = rob1[np.argmax(abs( s1[rob1]-s2[rob1]))]
        print(':(')
    else: print('Validity domain is empty!') #if V1 has no point with positive robustness
    
    
    ## With the procedure so far, a cell has been selected 
    ## ??? How to choose a particular parameter valuation?
    ## The  point in the middle of the cell
    parameters = [   ]
    nb_parameters = (len(V1.tensor[0])-1)//2
    
    # Points in the middle of the cell
    for par in range(nb_parameters):
        parameters.append(( float(V1.tensor[best_cell_index][par]) +float( V1.tensor[best_cell_index][par + nb_parameters]))/2)
    # parameters = [ V1.tensor[best_cell_index][0], V1.tensor[best_cell_index][1], V1.tensor[best_cell_index][6], V1.tensor[best_cell_index][7] ]
    return parameters #best_cell_index #

def ExtractParametersQuantitativeMultiple(V1, V2,  V3): #V1 vs (V2 u V3)
    
    ''' 
        N.B.
        The same partition of the parameters space is supposed for V1, V2, V3. 
        
        AND THE SAME ORDER!!!
        
        (This is always true when V1, V2, V3 came from the approximation with a fixed granularity.)
        If BinarySearch has been used, apply first the function AdaptGranularities.
    '''
    
    s1 = [] # s1 = vector of robustness values for V1
    for index_1 in range(len(V1.tensor)): 
        if V1.tensor[index_1][-1]!= 'undef':#float(V1.tensor[index_1][1]) < float(V1.tensor[index_1][2]): 
            s1.append(float(V1.tensor[index_1][-1]) )
        else: 
            s1.append(-1)
    s1 = np.array(s1)
    rob1 = np.where(s1 > 0)[0] #indices where V1 has positive robustness
    
    s2 = [] #s2 = vector of robustness values for V2, V3
    for index_2 in range(len(V2.tensor)):  #V1, V2, V3 have the same lenght by assumption
        if V1.tensor[index_1][-1]!= 'undef':#float(V1.tensor[index_2][1])< float(V1.tensor[index_2][2]):
            'When computing wrt 3 tensors'
            s2.append( max(float(V2.tensor[index_2][-1]), float(V3.tensor[index_2][-1]))) #
        else: 
            s2.append(1)
    s2 = np.array(s2)
    rob2 = np.where(s2 < 0)[0] #indices where max( V2, V3) has negative robustness
    
    intersection = list(set(rob1).intersection(rob2)) # indices of the intersection between rob1 and rob 2
    
    if len(intersection) > 0: # search among points with rob(V1) >=0 and rob(V2, V3)<=0
        best_cell_index = intersection[np.argmax(( s1[intersection]-s2[intersection]))]  
        print(s1[best_cell_index] - s2[best_cell_index])
        print(':)' )
    elif len(rob1)> 0: # otherwise, no restriction from V2/V3, but the point has to be in rob(V1)>=0 anyway
        best_cell_index = rob1[np.argmax(abs( s1[rob1]-s2[rob1]))]
        print(':(')
    else: print('Validity domain is empty!') #if V1 has no point with positive robustness
    
    
    ## With the procedure so far, a cell has been selected 
    ## ??? How to choose a particular parameter valuation?
    ## The  point in the middle of the cell
    parameters = [   ]
    nb_parameters = (len(V1.tensor[0])-1)//2
    
    # Points in the middle of the cell
    for par in range(nb_parameters):
        parameters.append(( float(V1.tensor[best_cell_index][par]) +float( V1.tensor[best_cell_index][par + nb_parameters]))/2)
    # parameters = [ V1.tensor[best_cell_index][0], V1.tensor[best_cell_index][1], V1.tensor[best_cell_index][6], V1.tensor[best_cell_index][7] ]
    return parameters #best_cell_index #


  