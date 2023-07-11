#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import csv
import os
import matlab as mat



def CollectAircraftData(n1, n2, fig, seed):
    
    ''' The function collect time_series from two different sets of airacraft data.
    
    INPUT:
        - n1: number of elements of the first kind of time_series
        - n2: number of elements of the second kind of time_series
        - fig: boolean value to decide wheter times series have to be plotted or not
        
    OUTPUT:
        - time_series: a list whose elements all the time series 
    
    '''
    
    path = '../../data/'
    # path = 'data/'
    
    np.random.seed(seed)
    
    time_series_class1 = []
    dataset_name = 'aircraft_amp_1_freq_p_correct'
    for p in range(1, 1 + n1):
        data = pd.read_csv(f"{path}{dataset_name}/aircraft_amp_1_freq_p_correct_{p}.csv")#, header = None)
        time_series_class1.append([list(range(len(data['lep_data'].values[::10]))),list(data['lep_data'].values[::10]), 1.1]) 
        if fig and p ==2:  plt.plot(data['lep_data'].values[::10], 'b', label='$S_1$')
 
    time_series_class2 = []
    dataset_name ='aircraft_amp_p_freq_1_tenth_correct'
    for p in range(1, 1 + n2):
        data = pd.read_csv(f"{path}{dataset_name}/aircraft_amp_p_freq_1_tenth_correct_{p}.csv")#, header = None)
        time_series_class2.append([list(range(len(data['lep_data'].values[::10]))),list(data['lep_data'].values[::10]),1.1])
        
        if fig and p ==1: plt.plot(data['lep_data'].values[::10], 'r', label='$S_2$')
    if fig:  
        plt.xlabel('t', fontsize = 70)    
        plt.ylabel('x', fontsize = 70)
        plt.xticks(fontsize=50)    
        plt.yticks(fontsize=50) 
        plt.legend(loc ='lower right', fontsize = 45)
        plt.savefig('aircraft_data.pdf',format='pdf', bbox_inches="tight")  
        
    np.random.shuffle(time_series_class1)
    np.random.shuffle(time_series_class2)
    
    return [time_series_class1, time_series_class2]


def StoreDataxenumerative_naval(indices_train, indices_test, data, times3, labels3, seed):
    
    file_name_data = f'store_data/data_seed_{seed}'
    file_name_labels = f'store_data/datalabels_seed_{seed}'
    # file_name_times = f'store_data/datatimes_blue_seed_{seed}'
    
    for i, indx in enumerate(indices_train):
        with open(f'{file_name_data}','a') as file:  
            for j in range(len(data[indx][0])): 
                file.write(f'{data[indx][0][j]} , {data[indx][1][j]} ')
                if j != len(data[indx][1])-1: file.write(' , ')
                else: file.write('\n')
        
        with open(f'{file_name_labels}','a') as file:  
            
            # if labels3[indx] == 1 : file.write(f'{float(1)}')
            # else: file.write(f'{float(-1)}')
            
            file.write(f'{float(labels3[indx])}')
        
        if i != len(indices_train) - 1:
            with open(f'{file_name_labels}','a') as file:  file.write(' , ')
        
        
    # with open(f'{file_name_times}','a') as file:  
    #     for i, item in enumerate(times3[0]):
    #         file.write(f'{float(item)}')
    #         if i!= len(times3[0]) -1 : file.write(' , ')


    # file_name_data = f'store_data/data_seed_{seed}'
    # file_name_labels = f'store_data/datalabels_seed_{seed}'
    # # file_name_times = f'store_data/datatimes_test_seed_{seed}'
    
    # for i, indx in enumerate(indices_test):
    #     with open(f'{file_name_data}','a') as file:  
    #         for j in range(len(data[indx][0])): 
    #             file.write(f'{data[indx][0][j]} , {data[indx][1][j]} ')
    #             if j != len(data[indx][1])-1: file.write(' , ')
    #             else: file.write('\n')
        
    #     with open(f'{file_name_labels}','a') as file:  
    #         # if labels3[indx] == 1 : file.write(f'{float(1)}')
    #         # else: file.write(f'{float(-1)}')
    #         file.write(f'{float(labels3[indx])}')
        
    #     if i != len(indices_train) - 1:
    #         with open(f'{file_name_labels}','a') as file:  file.write(' , ')
        
        
    # with open(f'{file_name_times}','a') as file:  
    #     for i, item in enumerate(times3[0]):
    #         file.write(f'{float(item)}')
    #         if i!= len(times3[0]) -1 : file.write(' , ')

    return

def StoreDataxGenetic_naval(indices_train, indices_test, data, labels3, seed):
    
    file_name_train = f'store_data/data_train_seed_{seed}.csv'
    file_name_test = f'store_data/data_test_seed_{seed}.csv'
    
    labels_train = []
    labels_test = []
    
    for indx in indices_train:
        aux = []
        for j in range(len(data[indx][0])): 
            aux.append(data[indx][0][j])
            aux.append(data[indx][1][j])
        
        with open(file_name_train, 'a', newline='') as file: 
            writer = csv.writer(file)
            writer.writerow(aux)
        
        if labels3[indx] == 1 : labels_train.append( 1 )
        else: labels_train.append( -1 )
   
    # for indx in indices_test:
    #       aux = []
    #       for j in range(len(data[indx][0])): 
    #           aux.append( data[indx][0][j] ) 
    #           aux.append( data[indx][1][j] )
          
    #       with open(file_name_test, 'a', newline='') as file: 
    #             writer = csv.writer(file)
    #             writer.writerow(aux)
        
    #       if labels3[indx] == 1 : labels_test.append( 1 )
    #       else: labels_test.append( -1 )
    
    with open(f'store_data/datalabels_train_seed_{seed}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(labels_train )
          
     
    # with open(f'store_data/datalabels_test_seed_{seed}.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(labels_test)
        
    return


def StoreDataxtree_naval(indices_train, indices_test, data, times3, labels3, seed):
    
    mdict ={'data'  : {'traces': [data[i] for i in indices_train] ,
            't'     : [float(item) for item in times3[0]] ,
            'labels':[[float(labels3[i]) for i in indices_train]] }}

    scipy.io.savemat(f'store_data/train_seed_{seed}.mat', mdict )   
    
    
    mdict = { 'data'  : {'traces': [data[i] for i in indices_test]  ,
              't'     : [float(item) for item in times3[0]] ,
              'labels': [float(labels3[i]) for i in indices_test] } }
    
    scipy.io.savemat(f'store_data/test_seed_{seed}.mat', mdict ) 
    
    return

def CollectNavalData(fig, seed, bool_store_data):
    
    np.random.seed(seed)
    
    ## Variables
    # pi[0] --> time
    # pi[1] --> x1
    # pi[2] --> x2
    # 
    path = '../../data/Naval/'
    
    # path = 'data/Naval/'
    
    naval3 = scipy.io.loadmat(f'{path}Naval_3C.mat')
    
    naval3 = naval3['data'][0][0]
    labels3 = naval3[2]
    times3 = naval3[1]
    data = naval3[0]
    
    colors = ['g','r','b']
    
    indices_class1 = []
    indices_class2 = []
    indices_class3 = []
    
    for i in range(len(data)):
        if fig: plt.plot(data[i][0], data[i][1], colors[int(labels3[i])-1])
        if  int(labels3[i])==1:   indices_class1.append(i)
            
        elif int(labels3[i])==2:  indices_class2.append(i)
        
        elif int(labels3[i])==3:  indices_class3.append(i)
           
    if fig:
        plt.savefig('naval_data.pdf', format='pdf')
        plt.show()
        
        
    ##Shuffle the time series (the seed is fixed by the script file)
    np.random.shuffle(indices_class1)
    np.random.shuffle(indices_class2)
    np.random.shuffle(indices_class3)

    
    time_series_class1 = []
    time_series_class2 = []
    time_series_class3 = []
    
    for index in indices_class1: time_series_class1.append([ list(range(len(data[index][0]))), data[index][0], data[index][1]])
    for index in indices_class2: time_series_class2.append([ list(range(len(data[index][0]))), data[index][0], data[index][1]])
    for index in indices_class3: time_series_class3.append([ list(range(len(data[index][0]))), data[index][0], data[index][1]])
    
    
    aux = set(indices_class1[:50])
    aux = aux.union(indices_class2[:50])
    aux = aux.union(indices_class3[:50])
    indices_train = list(aux)
    
    
    aux = set(indices_class1[50:])
    aux = aux.union(indices_class2[50:])
    aux = aux.union(indices_class3[50:])
    indices_test = list(aux)
    
    if bool_store_data: 
        if not os.path.exists('store_data'): os.mkdir('store_data')
        StoreDataxtree_naval(indices_train, indices_test, data, times3, labels3, seed)
        StoreDataxenumerative_naval(indices_train, indices_test, data, times3, labels3, seed)
        StoreDataxGenetic_naval(indices_train, indices_test, data, labels3, seed)
    
    if fig:
    #Print 30 time series
        for i in range(0,50):
            if i ==0:
                plt.plot(time_series_class1[i][1], time_series_class1[i][2], 'g', label = 'Regular behavior') #*
                plt.plot(time_series_class2[i][1], time_series_class2[i][2], 'r', label = 'Human trafficking') #+
                plt.plot(time_series_class3[i][1], time_series_class3[i][2], 'b',  label = 'Terrorism')#o
            else:
                plt.plot(time_series_class1[i][1], time_series_class1[i][2], 'g')#*
                plt.plot(time_series_class2[i][1], time_series_class2[i][2], 'r')#+
                plt.plot(time_series_class3[i][1], time_series_class3[i][2], 'b')#o
    
        plt.ylim(0, 50)       
        plt.xlabel('x1', fontsize = 60)
        plt.ylabel('x2', fontsize = 60) 
        plt.xticks(fontsize=60)    
        plt.yticks(fontsize=60) 
        plt.legend(loc ='lower right', fontsize = 35)
        
        plt.savefig('naval_time_series.pdf', format='pdf', bbox_inches="tight")
        plt.show()  
    
      
        
    return [time_series_class1, time_series_class2, time_series_class3]


def StoreDataxtree_parking(indices_train, indices_test, data, labels, seed):
    
    mdict ={'data'  : 
            { 'traces': [ [mat.double(data[i][2]), mat.double(data[i][3]), mat.double(data[i][4]),  mat.double([data[i][8]]*233)] for i in indices_train],
             't'     : data[0][0] , #[i for i in np.arange(0.05,11.7,0.05)], #
            'labels':[[float(labels[i]) for i in indices_train]] }}

    scipy.io.savemat(f'store_data/train_parking_seed_{seed}.mat', mdict )   
    
    
    mdict = { 'data'  : 
              {'traces':  [ [mat.double(data[i][2]), mat.double(data[i][3]), mat.double(data[i][4]),  mat.double([data[i][8]]*233)]  for i in indices_test]  ,
              't'     : data[0][0], #[i for i in np.arange(0.05,11.7,0.05)], #
              'labels': [float(labels[i]) for i in indices_test] } }
    
    scipy.io.savemat(f'store_data/test_parking_seed_{seed}.mat', mdict ) 
    
    return

def StoreDataxGenetic_parking(indices_train, indices_test, data, labels, seed):
    
    file_name_train = f'store_data/2var_parking_seed_{seed}.csv'
    # file_name_test = f'store_data/data_test_seed_{seed}.csv'
    
    labels_train = []
    times = [i for i in np.arange(0.05,11.7,0.05)]
    # labels_test = []
    
    for indx in indices_train:
        aux = []
        for j in range(len(data[indx][2])): 
            aux.append(data[indx][2][j])  # day+adult_clear: min = -49.99, max = -1.44 , day+clear+adult:mini = -49.99, -1.4221
            aux.append(data[indx][3][j])   # day+adult_clear : min = -0.0322 , max  = 10.980 day+clear+adult: mini = -0.032, maxi = 10.98
            # aux.append(data[indx][4][j])  # day+adult_clear:  mini = -32.57, max = 15.31 day+clear+adult: mini = -32.57, maxi 15.31
            # aux.append(data[indx][8]) # day+adult_clear: mini = -0.002, max = 4.317, day+clear+adult: mini = -0.01197, maxi = 4.1084
        
        with open(file_name_train, 'a', newline='') as file: 
            writer = csv.writer(file)
            writer.writerow(aux)
        
        if labels[indx] == 1 : labels_train.append( 1 )
        else: labels_train.append( -1 )
   
    # for indx in indices_test:
    #       aux = []
    #       for j in range(len(data[indx][2])): 
    #           aux.append( data[indx][2][j] ) 
    #           aux.append( data[indx][3][j] )
          
    #       with open(file_name_test, 'a', newline='') as file: 
    #             writer = csv.writer(file)
    #             writer.writerow(aux)
        
    #       if labels[indx] == 1 : labels_test.append( 1 )
    #       else: labels_test.append( -1 )
    
    with open(f'store_data/2var_parkinglabels_seed_{seed}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(labels_train )
          
        
    with open(f'store_data/parkingtimes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(times)
     
    # with open(f'store_data/datalabels_test_seed_{seed}.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(labels_test)
        
    return

def StoreDataxenumerative_parking(indices_train,  data,  labels3, seed):
    
    file_name_data = f'store_data/2var_parking_seed_{seed}'
    file_name_labels = f'store_data/2var_parkinglabels_seed_{seed}'
    
    for i, indx in enumerate(indices_train):
        with open(f'{file_name_data}','a') as file:  
            for j in range(len(data[indx][2])): 
                file.write(f'{data[indx][2][j]} , {data[indx][3][j]} ') #{data[indx][4][j]} {data[indx][8]} '
                if j != len(data[indx][2])-1: file.write(' , ')
                else: file.write('\n')
        
        
        with open(f'{file_name_labels}','a') as file:  
            
            if labels3[indx] == 1 : file.write(f'{float(1)}')
            else: file.write(f'{float(-1)}')
        
        if i != len(indices_train) - 1:
            with open(f'{file_name_labels}','a') as file:  file.write(' , ')
    
        
    times = [i for i in np.arange(0.05,11.7,0.05)]
    with open('store_data/parkingtimes', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(times)
    return


def CollectCarlaData(n, scenario, seed, bool_store_data, percentage_training):
    
    np.random.seed(seed)
    
    #Variables:
        # pi[0] time
        # pi[1] crash
        # pi[2] ego_y
        # pi[3] ego_v_y
        # pi[4] ego_a_y
        # pi[5] ped_x
        # pi[6] ped_v_x
        # pi[7] ped_y
        # pi[8] dist_crash
    
    path = '../../data/ParkingScenario/'
    # path = 'data/ParkingScenario/'
    dataset_name = 'disttrigger_'
    
    
    time_series_class1 = []
    time_series_class2 = []
    
    indices_class1 = []
    indices_class2 = []
    i = 0
    parking_data = []
    
    
    for p in range(0, n): 
    
        data = pd.read_csv(f"{path}{dataset_name}{p}.csv", header = None)
        
        
        ## DISCARD NIGHT DATA IN THE NEW DATA (NO HEADLIGHTS)
        if data[1][0].strip('][').split(', ')[0] != 'night':
    
    
            crash = (data[1][5].strip('][').split(', '))[0] 
            
            if crash == 'False': crash = False
            elif crash == 'True': crash = True
    
            time = [ float(item) for item in data[1][6].strip('][').split(', ')]
            
            ego_y = [ float(item) for item in data[1][8].strip('][').split(', ')]
            
            ego_v_y = [ float(item) for item in data[1][10].strip('][').split(', ') ]
            
            ego_a_y =  [ float(item) for item in data[1][12].strip('][').split(', ')]
            
            ped_x = [ float(item) for item in data[1][13].strip('][').split(', ') ]
            
            ped_v_x = [ float(item) for item in data[1][15].strip('][').split(', ') ]
            
            ped_y = [ float(item) for item in data[1][14].strip('][').split(', ') ]
            
            # dist_crash = (ego_v_y[-2]**2)/(2*abs(ego_a_y[-2]))
            # spec.declare_const('dist_crash', 'float', (x[3][-2]**2)/(2*(-x[4][-2])))
            
            
            ### !!! PADDING
            time = [i for i in np.arange(0.05,11.7,0.05)]
            for ele in range(233-len(ego_y)): 
                ego_y.append(ego_y[-1])
                ego_v_y.append(ego_v_y[-1])
                ego_a_y.append(ego_a_y[-1])
            
            dist_crash = (ego_v_y[-2]**2)/(2 *(- ego_a_y[-2])) #(x[3][-2]**2)/(2*(-x[4][-2])

            
            center_axes = -2.337 - 0.187
            
            if scenario == 'day+clear+adult':
     
                #Visibility
                if data[1][0].strip('][').split(', ')[0] == 'day'\
                   and data[1][1].strip('][').split(', ')[0] == 'clear'\
                   and data[1][2].strip('][').split(', ')[0] == 'adult':
                    
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y, ped_x, ped_v_x , ped_y , dist_crash, center_axes ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night'\
                   and data[1][1].strip('][').split(', ')[0] == 'fog'\
                   and data[1][2].strip('][').split(', ')[0] == 'child':
                        
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                
            elif scenario == 'day+clear':
                
                if data[1][0].strip('][').split(', ')[0] == 'day'\
                   and data[1][1].strip('][').split(', ')[0] == 'clear':
                        
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night'\
                   and data[1][1].strip('][').split(', ')[0] == 'fog':
                               
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                
            elif scenario == 'day_vs_night':
                if data[1][0].strip('][').split(', ')[0] == 'day':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night':
                    
                            
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
            elif scenario == 'day_vs_night_clear':
                if data[1][0].strip('][').split(', ')[0] == 'day'\
                and data[1][1].strip('][').split(', ')[0] == 'clear':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night' \
                  and data[1][1].strip('][').split(', ')[0] == 'clear':
                      
                            
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
            
            elif scenario == 'day_vs_night_fog_adult':
                if data[1][0].strip('][').split(', ')[0] == 'day'\
                and  data[1][1].strip('][').split(', ')[0] == 'fog'\
                and data[1][2].strip('][').split(', ')[0] == 'adult':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night' \
                  and data[1][1].strip('][').split(', ')[0] == 'fog'\
                  and data[1][2].strip('][').split(', ')[0] == 'adult':
                      
                            
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
            
            elif scenario == 'day_vs_night_fog_child':
                if data[1][0].strip('][').split(', ')[0] == 'day'\
                and data[1][1].strip('][').split(', ')[0] == 'fog'\
                and data[1][2].strip('][').split(', ')[0] == 'child':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night' \
                  and data[1][1].strip('][').split(', ')[0] == 'fog'\
                  and data[1][2].strip('][').split(', ')[0] == 'child':
                      
                            
                    indices_class2.append(i)
                    i += 1  
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y, dist_crash , center_axes  ])
                
                
            
            elif scenario == 'day+adult':
                if data[1][0].strip('][').split(', ')[0] == 'day' \
                and data[1][2].strip('][').split(', ')[0] == 'adult':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night' \
                    and data[1][2].strip('][').split(', ')[0] == 'child':
                        
                            
                    indices_class2.append(i)
                    i += 1    
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y , dist_crash, center_axes ])
            
            elif scenario == 'day+adult_clear':
                if data[1][0].strip('][').split(', ')[0] == 'day' \
                and data[1][2].strip('][').split(', ')[0] == 'adult'\
                     and data[1][1].strip('][').split(', ')[0] == 'clear':
                          
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night' \
                    and data[1][2].strip('][').split(', ')[0] == 'child'\
                     and data[1][1].strip('][').split(', ')[0] == 'clear':
                         
                                 
                        indices_class2.append(i)
                        i += 1
                        parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
            
            elif scenario == 'day+adult_fog':
                if data[1][0].strip('][').split(', ')[0] == 'day' \
                and data[1][2].strip('][').split(', ')[0] == 'adult'\
                     and data[1][1].strip('][').split(', ')[0] == 'fog':
                          
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y, dist_crash , center_axes  ])
                    
                elif data[1][0].strip('][').split(', ')[0] == 'night' \
                    and data[1][2].strip('][').split(', ')[0] == 'child'\
                     and data[1][1].strip('][').split(', ')[0] == 'fog':
                                 
                        indices_class2.append(i)
                        i += 1
                        parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
              
                
            elif scenario == 'clear_vs_fog_day':
                if data[1][1].strip('][').split(', ')[0] == 'clear'\
                and data[1][0].strip('][').split(', ')[0] == 'day':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                    
                elif data[1][1].strip('][').split(', ')[0] == 'fog'\
                and data[1][0].strip('][').split(', ')[0] == 'day':        
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y , dist_crash, center_axes ])
             
            elif scenario == 'clear+adult_day':
                if data[1][1].strip('][').split(', ')[0] == 'clear'\
                and data[1][2].strip('][').split(', ')[0] == 'adult'\
                and data[1][0].strip('][').split(', ')[0] == 'day':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                    
                elif data[1][1].strip('][').split(', ')[0] == 'fog'\
                 and data[1][2].strip('][').split(', ')[0] == 'child'\
                    and data[1][0].strip('][').split(', ')[0] == 'day':
                                
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y, dist_crash, center_axes  ])
              
            elif scenario == 'clear+adult_night':
                if data[1][1].strip('][').split(', ')[0] == 'clear'\
                and data[1][2].strip('][').split(', ')[0] == 'adult'\
                and data[1][0].strip('][').split(', ')[0] == 'night':
                     
                    indices_class1.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y, dist_crash , center_axes  ])
                    
                elif data[1][1].strip('][').split(', ')[0] == 'fog'\
                 and data[1][2].strip('][').split(', ')[0] == 'child'\
                    and data[1][0].strip('][').split(', ')[0] == 'night':
                                    
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y, dist_crash, center_axes ])
                
    
    
    dataset_name = 'disttrigger_lights_'
    
    for p in range(0, 800): 
    
        
        data = pd.read_csv(f"{path}{dataset_name}{p}.csv", header = None)
        
        crash = (data[1][5].strip('][').split(', '))[0]
        
        if crash == 'False': crash = False
        elif crash == 'True': crash = True

        time = [ float(item) for item in data[1][6].strip('][').split(', ')]
        
        ego_y = [ float(item) for item in data[1][8].strip('][').split(', ')]
        
        ego_v_y = [ float(item) for item in data[1][10].strip('][').split(', ') ]
        
        ego_a_y =  [ float(item) for item in data[1][12].strip('][').split(', ')]
        
        ped_x = [ float(item) for item in data[1][13].strip('][').split(', ') ]
        
        ped_v_x = [ float(item) for item in data[1][15].strip('][').split(', ') ]
        
        ped_y = [ float(item) for item in data[1][14].strip('][').split(', ') ]
        
        ### !!! PADDING
        time = [i for i in np.arange(0.05,11.7,0.05)]
        for ele in range(233-len(ego_y)):  
                ego_y.append(ego_y[-1])
                ego_v_y.append(ego_v_y[-1])
                ego_a_y.append(ego_a_y[-1])
        
        dist_crash = (ego_v_y[-2]**2)/(2 *(- ego_a_y[-2])) #(x[3][-2]**2)/(2*(-x[4][-2])
        
        if scenario == 'day+clear+adult':
 
            #Visibility
            if data[1][0].strip('][').split(', ')[0] == 'day'\
               and data[1][1].strip('][').split(', ')[0] == 'clear'\
               and data[1][2].strip('][').split(', ')[0] == 'adult':
                    
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night'\
               and data[1][1].strip('][').split(', ')[0] == 'fog'\
               and data[1][2].strip('][').split(', ')[0] == 'child':
                               
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
            
        elif scenario == 'day+clear':
            
            if data[1][0].strip('][').split(', ')[0] == 'day'\
               and data[1][1].strip('][').split(', ')[0] == 'clear':
                    
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night'\
               and data[1][1].strip('][').split(', ')[0] == 'fog':
                   
                 
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
            
        elif scenario == 'day_vs_night':
            if data[1][0].strip('][').split(', ')[0] == 'day':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night':
                            
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                
        elif scenario == 'day_vs_night_clear':
            if data[1][0].strip('][').split(', ')[0] == 'day'\
            and data[1][1].strip('][').split(', ')[0] == 'clear':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash, center_axes  ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night' \
              and data[1][1].strip('][').split(', ')[0] == 'clear':
                              
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash, center_axes  ])
        
        elif scenario == 'day_vs_night_fog_adult':
            if data[1][0].strip('][').split(', ')[0] == 'day'\
            and  data[1][1].strip('][').split(', ')[0] == 'fog'\
            and data[1][2].strip('][').split(', ')[0] == 'adult':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y  ,dist_crash, center_axes  ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night' \
              and data[1][1].strip('][').split(', ')[0] == 'fog'\
              and data[1][2].strip('][').split(', ')[0] == 'adult':
                              
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
        
        elif scenario == 'day_vs_night_fog_child':
            if data[1][0].strip('][').split(', ')[0] == 'day'\
            and data[1][1].strip('][').split(', ')[0] == 'fog'\
            and data[1][2].strip('][').split(', ')[0] == 'child':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night' \
              and data[1][1].strip('][').split(', ')[0] == 'fog'\
              and data[1][2].strip('][').split(', ')[0] == 'child':
                              
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
            
            
        
        elif scenario == 'day+adult':
            if data[1][0].strip('][').split(', ')[0] == 'day' \
            and data[1][2].strip('][').split(', ')[0] == 'adult':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y, dist_crash , center_axes  ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night' \
                and data[1][2].strip('][').split(', ')[0] == 'child':
                                
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y , dist_crash, center_axes ])
        
        elif scenario == 'day+adult_clear':
            if data[1][0].strip('][').split(', ')[0] == 'day' \
            and data[1][2].strip('][').split(', ')[0] == 'adult'\
                 and data[1][1].strip('][').split(', ')[0] == 'clear':
                      
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash, center_axes  ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night' \
                and data[1][2].strip('][').split(', ')[0] == 'child'\
                 and data[1][1].strip('][').split(', ')[0] == 'clear':
                            
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash , center_axes  ])
        
        elif scenario == 'day+adult_fog':
            if data[1][0].strip('][').split(', ')[0] == 'day' \
            and data[1][2].strip('][').split(', ')[0] == 'adult'\
                 and data[1][1].strip('][').split(', ')[0] == 'fog':
                      
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y , dist_crash , center_axes ])
                
            elif data[1][0].strip('][').split(', ')[0] == 'night' \
                and data[1][2].strip('][').split(', ')[0] == 'child'\
                 and data[1][1].strip('][').split(', ')[0] == 'fog':
                            
                    indices_class2.append(i)
                    i += 1
                    parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash , center_axes ])
          
            
        elif scenario == 'clear_vs_fog_day':
            if data[1][1].strip('][').split(', ')[0] == 'clear'\
            and data[1][0].strip('][').split(', ')[0] == 'day':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash, center_axes  ])
                
            elif data[1][1].strip('][').split(', ')[0] == 'fog'\
            and data[1][0].strip('][').split(', ')[0] == 'day':
                       
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y, dist_crash, center_axes  ])
         
        elif scenario == 'clear+adult_day':
            if data[1][1].strip('][').split(', ')[0] == 'clear'\
            and data[1][2].strip('][').split(', ')[0] == 'adult'\
            and data[1][0].strip('][').split(', ')[0] == 'day':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash, center_axes  ])
                
            elif data[1][1].strip('][').split(', ')[0] == 'fog'\
             and data[1][2].strip('][').split(', ')[0] == 'child'\
                and data[1][0].strip('][').split(', ')[0] == 'day':
                           
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y ,dist_crash, center_axes ])
          
        elif scenario == 'clear+adult_night':
            if data[1][1].strip('][').split(', ')[0] == 'clear'\
            and data[1][2].strip('][').split(', ')[0] == 'adult'\
            and data[1][0].strip('][').split(', ')[0] == 'night':
                 
                indices_class1.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x , ped_y ,dist_crash, center_axes  ])
                
            elif data[1][1].strip('][').split(', ')[0] == 'fog'\
             and data[1][2].strip('][').split(', ')[0] == 'child'\
                and data[1][0].strip('][').split(', ')[0] == 'night':
                     
                indices_class2.append(i)
                i += 1
                parking_data.append([time ,crash,  ego_y, ego_v_y, ego_a_y,ped_x, ped_v_x  , ped_y , dist_crash , center_axes ])
    
            
    ##Shuffle the time series (the seed is fixed by the script file)
    np.random.shuffle(indices_class1)
    np.random.shuffle(indices_class2)

    
    time_series_class1 = []
    time_series_class2 = []
    labels = ['a'] * len(parking_data)
    
    for index in indices_class1: 
            time_series_class1.append(parking_data[index])
            labels[index]  = 1
    for index in indices_class2:
            time_series_class2.append(parking_data[index])
            labels[index] = 2
            
    n_train = int(len(indices_class1)* percentage_training/100) 
    
    aux = set(indices_class1[:n_train])
    aux = aux.union(indices_class2[:n_train])
    indices_train = list(aux)
    
    
    aux = set(indices_class1[n_train:])
    aux = aux.union(indices_class2[n_train:])
    indices_test = list(aux)
    
    if bool_store_data: 
        if not os.path.exists('store_data'): os.mkdir('store_data')
        # StoreDataxtree_parking(indices_train, indices_test, parking_data, labels, seed)
        # StoreDataxGenetic_parking(indices_train, indices_test, parking_data, labels, seed)
        StoreDataxenumerative_parking(indices_train,  parking_data, labels, seed)
    return [time_series_class1, time_series_class2]
   




