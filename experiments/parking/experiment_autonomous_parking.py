#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
sys.path.insert(0, '../../')

import time
import numpy as np

import time_series_collection as tsc
import inputs
import parameter_mining



## SPEC (V_safe, dist_safe)  
#  spec.spec = f'(always(ego_y  <= {-param[1]-2.337-0.187})) or (eventually(ego_v_y>= {param[0]}))'
 
## SPEC (V_UNsafe, dist_UNsafe)
#  spec.spec = f'((always(ego_v_y <= {param[0]})) or  (dist_crash>= {param[1]}))'
  

#############################
### First experiment #####
############################
#seed = [ [13,17] , [3, 4], [78,2], [111, 23],[81, 18]  ]


##First run: adult crossing the parking lot during the day versus a child pedes- trian at night

#scenarios = ['day+adult_clear']#,day+clear+adult', 'day+adult_fog', 'clear+adult_day', 'clear+adult_night', 'clear_vs_fog_day']#, 'day_vs_night_clear', 'day_vs_night_fog_adult', 'day_vs_night_fog_child']
    
## DAY ADULT VS CHILD AT NIGHT WITH CLEAR SKY

data_seed_1 = 885736 #np.random.randint(0, 1000000)
learning_seed_1 = 839131#np.random.randint(0, 1000000)
bool_store_data = True
percentage_training = 80

traces = tsc.CollectCarlaData(1600, 'day+adult_clear',data_seed_1 ,  bool_store_data, percentage_training)

file_name = 'Parking_80perc.text'
start_time_learning_1 = time.time()
   
k = 5
par_bounds = [   [5.55,11.09], [1, 7]]
granularity = [(par_bounds[0][1]-par_bounds[0][0])/(2**k),(par_bounds[1][1]-par_bounds[1][0])/(2**k)]

p_formula = '(always( pi[2] <= - epsilon1- + pi[9]  )) or (eventually( pi[3] >= epsilon0- ))'

# p_formula = '( pi[1] ) or ((always( pi[2] <= - epsilon1- + pi[9]  )) or (eventually( pi[3] >= epsilon0- )))'


with open(f'{file_name}','a') as file: 
    file.write('n_train= 80 perc\n\n\n')
    file.write(f'\n\n\nExperiment 1: scenario day+adult_clear vs night+child_clear\n\n PSTL template1: {p_formula}')

input_data = inputs.InputData(
    seed = learning_seed_1, 
    traces = traces, 
    p_formula = p_formula , 
    par_bounds = par_bounds, 
    granularity = granularity , 
    sampling_freq = [0.05,'s', 0.01], 
    )


input_data.bool_plot_figure = True
input_data.bool_store_results = True
input_data.bool_different_templates = True
input_data.file_name = f'{file_name}'
input_data.percentage_training = percentage_training

input_data.bool_mono = True 
input_data.mono = [  -1, -1  ] 
input_data.bool_domain_knowledge = True
input_data.constant_definition = [ [9, 'float' ]] #[1, 'bool'],         # pi[9] = -2.337 - 0.187 #centering of the axis


p_formula2 =  '((always( pi[3] <= epsilon0- )) or  ( pi[8] >= epsilon1- ))' #pi[8] = dist crash

# p_formula2 =  '(not( pi[1] )) or ((always( pi[3] <= epsilon0- )) or  ( pi[8] >= epsilon1- ))' #pi[8] = dist crash


with open(f'{file_name}','a') as file: file.write(f'\n PSTL template2: {p_formula2}')

input_data.p_formula2 = p_formula2
par_bounds2 = [   [5.55,11.09], [0, 7]]
input_data.par_bounds2 = par_bounds2
input_data.granularity2 = [(par_bounds2[0][1]-par_bounds2[0][0])/(2**k),(par_bounds2[1][1]-par_bounds2[1][0])/(2**k)]
input_data.sampling_freq2 = [0.05,'s', 0.01]
input_data.constant_definition2 = [[8, 'float'] ] #, [1, 'bool'] ]
input_data.bool_mono2 = True
input_data.mono2 =  [  1, -1  ]

# spec.declare_const('crash', 'bool', x[1])
# if x[1] == True: spec.declare_const('not_crash', 'bool', False)
# elif x[1] == False: spec.declare_const('not_crash', 'bool',True)
 

# spec.declare_const('dist_crash', 'float', (x[3][-2]**2)/(2*(-x[4][-2])))
 #constant_definition = [indx, type ]    

parameter_mining.main(input_data)

end_time_learning_1 = time.time()  
time_learning_1 = end_time_learning_1 - start_time_learning_1

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_1 = {time_learning_1}')
    
    file.write(f'\ndata_seed_1 = {data_seed_1}')
    file.write(f'\nlearning_seed_1 = {learning_seed_1}')

     
#############################
### Second experiment #####
############################
    

## Second run: 
## DAY ADULT WITH CLEAR SKY VS CHILD AT NIGHT WITH FOG

with open(f'{file_name}','a') as file: 
    file.write(f'\n\n\nExperiment 2: scenario day+adult+clear vs night+child+fog\n\n PSTL template1: {p_formula}')
    file.write(f'\n PSTL template2: {p_formula2}')


data_seed_2 = 350353#np.random.randint(0, 1000000)
learning_seed_2 = 833453#np.random.randint(0, 1000000)

traces = tsc.CollectCarlaData(1600, 'day+clear+adult',  data_seed_2 ,  bool_store_data, percentage_training)  
input_data.seed =  learning_seed_2
input_data.traces = traces

start_time_learning_2 = time.time()
    
parameter_mining.main(input_data)

end_time_learning_2 = time.time()

time_learning_2 = end_time_learning_2 - start_time_learning_2

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_2 = {time_learning_2}')
    
    file.write(f'\ndata_seed_2 = {data_seed_2}')
    file.write(f'\nlearning_seed_2 = {learning_seed_2}')


                