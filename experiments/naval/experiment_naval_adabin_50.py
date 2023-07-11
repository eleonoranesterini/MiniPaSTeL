#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../../')


import numpy as np
import time

import time_series_collection as tsc
import inputs
import parameter_mining


##########################################
##########  Experiment 1    ##############
##########################################


p_formula = '(( pi[2] > epsilon0- )until[epsilon1- : epsilon2- ]( pi[1] <= epsilon3- ))'

n_train = [50,50,50]

file_name = f'Naval{n_train[0]}_AdaBin.text'

# seed = [[5,5,5]]#[ [41, 50, 2], [66, 17, 94], [56, 12, 9], [18, 3 ,1], [74, 42, 20]]

data_seed_1 = 8868#np.random.randint(0, 1000000)
learning_seed_1 = 132589#np.random.randint(0, 1000000)

start_time_learning_1 = time.time()

#Naval Data
fig = False
traces =   tsc.CollectNavalData(fig , data_seed_1, False)


with open(f'{file_name}','a') as file: 
    file.write(f'n_train={n_train}\n\n\n')
    file.write(f'\n\n\nExperiment 1:\nPSTL template: {p_formula}\n')
    

input_data = inputs.InputData(
    seed = learning_seed_1 , 
    traces = traces ,  
    p_formula = p_formula, 
    par_bounds = [ [17, 46] , [0,60], [0,60], [3, 81] ], 
    granularity  = [1.8125 , 3.75 ,3.75 ,4.875 ],  
    sampling_freq = [1, 's', 0.1])

input_data.bool_mono = True
input_data.mono = [-1, -1, 1, 1]
input_data.bool_binarysearch = True 

input_data.bool_plot_figure = fig
input_data.bool_store_results = True
        
input_data.numb_train = n_train
input_data.file_name = f'{file_name}'


parameter_mining.main(input_data)

end_time_learning_1 = time.time()  
time_learning_1 = end_time_learning_1 - start_time_learning_1 

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_1 = {time_learning_1}')
    
    file.write(f'\ndata_seed_1 = {data_seed_1}')
    file.write(f'\nlearning_seed_1 = {learning_seed_1}')
    
    
##########################################
##########  Experiment 2    ##############
##########################################


p_formula = '(( pi[2] > epsilon0- )until[epsilon1- : epsilon2- ]( pi[1] <= epsilon3- ))'

data_seed_2 = 470380#np.random.randint(0, 1000000)
learning_seed_2 = 958704 #np.random.randint(0, 1000000)

start_time_learning_2 = time.time()

#Naval Data
fig = False
traces =   tsc.CollectNavalData(fig , data_seed_2, False)


with open(f'{file_name}','a') as file:  file.write(f'\n\n\nExperiment 2:\nPSTL template: {p_formula}\n')
    

input_data = inputs.InputData(
    seed = learning_seed_2 , 
    traces = traces ,  
    p_formula = p_formula, 
    par_bounds = [ [17, 46] , [0,60], [0,60], [3, 81] ], 
    granularity  = [1.8125 , 3.75 ,3.75 ,4.875 ],  
    sampling_freq = [1, 's', 0.1])

input_data.bool_mono = True
input_data.mono = [-1, -1, 1, 1]
input_data.bool_binarysearch = True 

input_data.bool_plot_figure = fig
input_data.bool_store_results = True
        
input_data.numb_train = n_train
input_data.file_name = f'{file_name}'


parameter_mining.main(input_data)

end_time_learning_2 = time.time()  
time_learning_2 = end_time_learning_2 - start_time_learning_2 

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_2 = {time_learning_2}')
    
    file.write(f'\ndata_seed_2 = {data_seed_2}')
    file.write(f'\nlearning_seed_2 = {learning_seed_2}')
    


##########################################
##########  Experiment 3    ##############
##########################################


p_formula = '(( pi[2] > epsilon0- )until[epsilon1- : epsilon2- ]( pi[1] <= epsilon3- ))'

data_seed_3 = 924934#np.random.randint(0, 1000000)
learning_seed_3 = 244962#np.random.randint(0, 1000000)

start_time_learning_3 = time.time()

#Naval Data
fig = False
traces =   tsc.CollectNavalData(fig , data_seed_3, False)


with open(f'{file_name}','a') as file:  file.write(f'\n\n\nExperiment 3:\nPSTL template: {p_formula}\n')
    

input_data = inputs.InputData(
    seed = learning_seed_3 , 
    traces = traces ,  
    p_formula = p_formula, 
    par_bounds = [ [17, 46] , [0,60], [0,60], [3, 81] ], 
    granularity  = [1.8125 , 3.75 ,3.75 ,4.875 ],  
    sampling_freq = [1, 's', 0.1])

input_data.bool_mono = True
input_data.mono = [-1, -1, 1, 1]
input_data.bool_binarysearch = True 

input_data.bool_plot_figure = fig
input_data.bool_store_results = True
        
input_data.numb_train = n_train
input_data.file_name = f'{file_name}'


parameter_mining.main(input_data)

end_time_learning_3 = time.time()  
time_learning_3 = end_time_learning_3 - start_time_learning_3 

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_3 = {time_learning_3}')
    
    file.write(f'\ndata_seed_3 = {data_seed_3}')
    file.write(f'\nlearning_seed_3 = {learning_seed_3}')
    


##########################################
##########  Experiment 4    ##############
##########################################


p_formula = '(( pi[2] > epsilon0- )until[epsilon1- : epsilon2- ]( pi[1] <= epsilon3- ))'

data_seed_4 = 505971#np.random.randint(0, 1000000)
learning_seed_4 = 245407#np.random.randint(0, 1000000)

start_time_learning_4 = time.time()

#Naval Data
fig = False
traces =   tsc.CollectNavalData(fig , data_seed_4, False)


with open(f'{file_name}','a') as file:  file.write(f'\n\n\nExperiment 4:\nPSTL template: {p_formula}\n')
    

input_data = inputs.InputData(
    seed = learning_seed_4 , 
    traces = traces ,  
    p_formula = p_formula, 
    par_bounds = [ [17, 46] , [0,60], [0,60], [3, 81] ], 
    granularity  = [1.8125 , 3.75 ,3.75 ,4.875 ],  
    sampling_freq = [1, 's', 0.1])

input_data.bool_mono = True
input_data.mono = [-1, -1, 1, 1]
input_data.bool_binarysearch = True 

input_data.bool_plot_figure = fig
input_data.bool_store_results = True
        
input_data.numb_train = n_train
input_data.file_name = f'{file_name}'


parameter_mining.main(input_data)

end_time_learning_4 = time.time()  
time_learning_4 = end_time_learning_4- start_time_learning_4

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_4 = {time_learning_4}')
    
    file.write(f'\ndata_seed_4 = {data_seed_4}')
    file.write(f'\nlearning_seed_4 = {learning_seed_4}')
    


##########################################
##########  Experiment 5    ##############
##########################################


p_formula = '(( pi[2] > epsilon0- )until[epsilon1- : epsilon2- ]( pi[1] <= epsilon3- ))'

data_seed_5 = 16038#np.random.randint(0, 1000000)
learning_seed_5 = 903230#np.random.randint(0, 1000000)

start_time_learning_5 = time.time()

#Naval Data
fig = False
traces =   tsc.CollectNavalData(fig , data_seed_5, False)


with open(f'{file_name}','a') as file:  file.write(f'\n\n\nExperiment 5:\nPSTL template: {p_formula}\n')
    

input_data = inputs.InputData(
    seed = learning_seed_5 , 
    traces = traces ,  
    p_formula = p_formula, 
    par_bounds = [ [17, 46] , [0,60], [0,60], [3, 81] ], 
    granularity  = [1.8125 , 3.75 ,3.75 ,4.875 ],  
    sampling_freq = [1, 's', 0.1])

input_data.bool_mono = True
input_data.mono = [-1, -1, 1, 1]
input_data.bool_binarysearch = True 

input_data.bool_plot_figure = fig
input_data.bool_store_results = True
        
input_data.numb_train = n_train
input_data.file_name = f'{file_name}'


parameter_mining.main(input_data)

end_time_learning_5 = time.time()  
time_learning_5 = end_time_learning_5- start_time_learning_5 

with open(f'{file_name}','a') as file: 
    
    file.write(f'\ntime_learning_5 = {time_learning_5}')
    
    file.write(f'\ndata_seed_5 = {data_seed_5}')
    file.write(f'\nlearning_seed_5 = {learning_seed_5}')
    

