#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../../')

import inputs
import time_series_collection as tsc
import parameter_mining
import numpy as np
import time

##############################
##### Experiment spec 1 ######
##############################

## Data from Aircraft

# seed = [[5,5,5]]#[ [41, 50, 2], [66, 17, 94], [56, 12, 9], [18, 3 ,1], [74, 42, 20]]

data_seed_1 = np.random.randint(0, 1000000)
learning_seed_1 = np.random.randint(0, 1000000)

start_time_learning_1 = time.time()


n1 = 10 #3 #elements in class 1
n2 = 10 #3 #elements in class 2
n = n1 + n2 #total number of signals
fig = True #whether time series have to be plotted or not
traces = tsc.CollectAircraftData(n1, n2, fig, data_seed_1)

file_name = f'Aircraft{n1}AdaBin.text'

## SPEC 1
## Always( (x >= p) -> always[0,T]( abs(x - p) < 0.5) )
p_formula = ' always( ( pi[1] >= epsilon1- ) implies (always[0 : epsilon0- ] ( abs( pi[1] - epsilon1- ) < 0.5  )))' 


with open(f'{file_name}','a') as file: 
    file.write(f'n_train=[{n1},{n2}]\n\n\n')
    file.write(f'\n\n\nExperiment 1:\n\n PSTL template: {p_formula}')

input_data = inputs.InputData(
    seed = learning_seed_1 ,
    traces = traces, 
    p_formula =  p_formula , 
    par_bounds = [ [ 0, 1000 ] , [-1.6,1.6]], 
    granularity  = [ 31.25, 0.1],  #k =5 #(2^k)
    sampling_freq = [ 1,'s', 0.1])


input_data.bool_plot_figure = fig
input_data.bool_store_results = True
input_data.percentage_training = 100
input_data.bool_binarysearch = True

input_data.file_name = f'{file_name}'

parameter_mining.main(input_data)


end_time_learning_1 = time.time()  
time_learning_1 = end_time_learning_1 - start_time_learning_1 

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_1 = {time_learning_1}')
    file.write(f'\ndata_seed_1 = {data_seed_1}')
    file.write(f'\nlearning_seed_1 = {learning_seed_1}')

##############################
##### Experiment spec 2 ######
##############################

learning_seed_2 = np.random.randint(0, 1000000)
start_time_learning_2 = time.time()

## SPEC  2 
p_formula = ' always( ( pi[1] >= pi[2] ) implies (always[0: epsilon0- ](  abs( pi[1] - pi[2] ) < 0.5 )   and (always[ epsilon1- : epsilon0- + epsilon1- ](  abs(pi[1] - pi[2] ) > 0.5))))'          
 

with open(f'{file_name}','a') as file: 
    file.write(f'\n\n\nExperiment 2 :\n\n PSTL template: {p_formula}')

input_data = inputs.InputData(
    seed = learning_seed_2 ,
    traces = traces, 
    p_formula =  p_formula , 
    par_bounds = [ [ 0, 1000 ] , [0, 1000 ]], 
    granularity  = [ 7.8125  , 7.8125], # k =7 #(2^k)
    sampling_freq = [ 1,'s', 0.1])


input_data.bool_plot_figure = fig
input_data.bool_store_results = True
input_data.percentage_training = 100
input_data.bool_binarysearch = True
input_data.file_name = f'{file_name}'
input_data.constant_definition = [[2, 'float' ]] # pi[2] = 1.1


parameter_mining.main(input_data)

end_time_learning_2 = time.time()  
time_learning_2 = end_time_learning_2 - start_time_learning_2 

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_2 = {time_learning_2}')
    
    file.write(f'\nlearning_seed_2 = {learning_seed_2}')
