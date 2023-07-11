import sys
sys.path.insert(0, 'rtamt/')

import rtamt
import numpy as np
from rtamt.spec.stl.discrete_time.specification import Semantics

import time_series_collection as tsc

def instantiate_formula(p_formula, parameter):
        
    ''' The function replaces the parameter symbols in the parametric formula
    with a concrete formula using the given parameter'''     
    
    formula = p_formula
    
    for i in range(20): 
        if f'epsilon{i}-' in formula: formula = formula.replace(f'epsilon{i}-',f'{str(parameter[i])}')
    return formula

def check_timimg_bound(formula, max_time):
    
    '''1) Check whether in a time bound [a:b] a is greater than b. 
    If so, bool_compute_rob= False and no computation of the robustness is done
    
       2) Check whether in a time bound [a:b] b is greater than the time horizon admissible.
    If so, b is replaced with maximum admissible time and bool_compute_rob = True --> robustness is computed
    
        3) Check whether mathematical operations are included in the temporal range. If so, they are replaced with its numerical value
    
    '''
    
    bool_compute_rob = True
    new_formula = formula
    sub_formula = formula
    characters_removed = 0
    
    while True:
    
        start = sub_formula.find('[')
        #Stop when there are no more temporal parameters
        if start < 0 : break
        
        end = sub_formula.find(']')
        bounds = sub_formula[start+1 : end].split(':')
        
        #End with 'unsuccess' because [a:b] with a >= b
        if float(eval(bounds[0])) >= float(eval(bounds[1])): return False, new_formula

        
        #Change bounds[1] to max_time
        if float(eval(bounds[1])) > max_time: 
            sep = sub_formula.find(':')
            new_formula = new_formula[:characters_removed + sep + 1]+ f'{max_time}' +new_formula[characters_removed + end:]
            sub_formula = sub_formula[: sep + 1]+ f'{max_time}' + sub_formula[end:]
            end = sub_formula.find(']')
            
        sub_formula = sub_formula[end+1:]
        characters_removed += len(sub_formula[:end+1])
    
    characters_removed = 0    
    sub_formula = new_formula    
    while True:
    
        start = sub_formula.find('[')
        #Stop when there are no more temporal parameters
        if start < 0 : return bool_compute_rob, new_formula 
        
        end = sub_formula.find(']')
        bounds = sub_formula[start+1 : end].split(':')
        
        if '+' in bounds[0] or '-' in bounds[0]: 
            sep = sub_formula.find(':')
            new_formula = new_formula[:characters_removed + start + 1]+ f'{float(eval(bounds[0]))}' +new_formula[characters_removed + sep:]
            sub_formula = sub_formula[: start + 1]+ f'{float(eval(bounds[0]))}' + sub_formula[sep:]
         
            
        if '+' in bounds[1] or '-' in bounds[1]: 
            sep = sub_formula.find(':')
            new_formula = new_formula[:characters_removed + sep + 1]+ f'{float(eval(bounds[1]))}' +new_formula[characters_removed + end:]
            sub_formula = sub_formula[: sep + 1]+ f'{float(eval(bounds[1]))}' + sub_formula[end:]
            end = sub_formula.find(']')
            
        sub_formula = sub_formula[end+1:]
        characters_removed += len(sub_formula[:end+1])
    

   

def EvaluateRob(pi, formula, sampling_freq, constant_definition ):
    
    ''' INPUT:
        - pi : time series
        - formula : stl formula
        
        OUTPUT:
        - rho: robustness of STL_phi in pi[0] (first time value)
    '''
 
    
    new_formula = formula.replace('pi[','pi_')

    # Indices of where the 'pi' start
    variable_indices = [i for i in range(len(new_formula)) if new_formula.startswith('pi', i)]
    
    spec = rtamt.STLSpecification(language=rtamt.Language.PYTHON)
    spec.name = 'STL Discrete-time Offline monitor'
    spec.set_sampling_period(sampling_freq[0], sampling_freq[1] , sampling_freq[2])
    
    dataSet = { 'time': list(pi[0])}
    
    already_declared = []
    
    #constant_definition = [indx, type ] 
    for item in constant_definition:
            indx = item[0]
            spec.declare_const(f'pi_{indx}', item[1], pi[int(indx)] )
            ## !!!
            # dataSet.update({f'pi_{indx}' : pi[int(indx)][0]})
            already_declared.append(f'{indx}')
    
    for item in  variable_indices:
        indx = new_formula[item + 3] # +3 because it is the length of the string 'pi_'
        end = 4 # the index has at least length 1 ( = 4-3 )
        while True : # find the end of first index 
            if new_formula[item + end] == ']' or new_formula[item + end] == ')': break #ends when ' ' or ')' appear
            end += 1
        indx = int(new_formula[item + 3: item + end]  )
        
        #Remove ']' at the end of pi[i], but not ']' closing a timing interval
        new_formula = new_formula[:item + end]+ ' ' + new_formula[item + end +1:]
        
        
        #Avoid already declared pairs of indices
        if f'{indx}' not in already_declared:
        
            spec.declare_var(f'pi_{indx}', 'float')
        
            dataSet.update({f'pi_{indx}' : pi[int(indx)]})
            
            already_declared.append(f'{indx}')
      
            
    ## !!! -2 ??
    max_time = pi[0][-1] 
    bool_compute_rob, new_formula = check_timimg_bound(new_formula, max_time)        
    if not bool_compute_rob: return 'undef'  
            
    spec.spec = new_formula
    spec.semantics = Semantics.STANDARD
    
    try:
        spec.parse()
        
    except rtamt.STLParseException as err:
        print(new_formula)
        print('STL Parse Exception: {}'.format(err))
        sys.exit()
        
    rho = spec.evaluate(dataSet)
    
    return rho[0][1]
    
    
    spec.semantics = Semantics.STANDARD
    
    try:
        spec.parse()
        
    except rtamt.STLParseException as err:
        print('STL Parse Exception: {}'.format(err))
        print('Formula =', formula )
        sys.exit()
    robustness = spec.evaluate(dataSet)
    ## output is :[  [time, rob(time)]  , .., ..] --> we are interested in time = 0
    # robustness[0][1]: [0] because we want time=0, [1] because we want the second value in the pair (the robustness value)
    rho = robustness[0][1]
    return  rho

  