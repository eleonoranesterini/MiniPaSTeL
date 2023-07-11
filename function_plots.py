#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import function as fun
# import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os 



def CreatePoly(points, alpha , color):
    
    ''''The function creates the colored parallelepiped for the cell described by the list of 3d points.'''
    
     
    v = np.array([[     points[0] , points[1], points[2]]  ,   
                  [     points[0] , points[1], points[5] ]  ,
                  [     points[3] , points[1], points[2] ],
                  [     points[3] , points[1], points[5] ],
                  [     points[0] , points[4], points[2] ],
                  [     points[0] , points[4], points[5] ],
                  [     points[3] , points[4], points[2] ],
                  [     points[3] , points[4], points[5] ] ] )
    
    vertices = [[  v[0], v[1], v[3], v[2]   ],
                [  v[4], v[5], v[7], v[6]   ],
                [  v[2], v[3], v[7], v[6]   ],
                [  v[0], v[4], v[5], v[1]   ],
                [  v[0], v[2], v[6], v[4]   ],
                [  v[1], v[3], v[7], v[5]   ]  ]
    
    poly = Poly3DCollection(vertices, alpha= alpha, color = color)
    
    return poly


def PlotVals_2or3dim(par_bound, V, ax,  given_color , given_alpha):
    
    if len(par_bound) == 2:
        
            
        for i in range(len(V.tensor)):
            if  V.tensor[i][-1] == 'undef': #undefined: part of the parameter space that is not studied
                color = 'k'
                alpha = 1
            
            elif float(V.tensor[i][-1]) < 0. : # not satisfied
                color = given_color #'b'
                alpha = 0 
            elif float(V.tensor[i][-1]) > 0. : # satisfied 
                alpha = given_alpha 
                color = given_color #'b'
            elif float(V.tensor[i][-1]) == 0.:  # grey situation 
                alpha = 0 
                color = 'grey'
            
            
            #To plot space with letf-bottom point (x_min,y_min) and right-top (x_max, y_max):
            #ax.fill([x_min, x_max], [y_max, y_max], [y_min, y_min])
            ax.fill_between([V.tensor[i][0], V.tensor[i][2]], [V.tensor[i][3], V.tensor[i][3]], [V.tensor[i][1], V.tensor[i][1]], alpha = alpha, color = color)
            # ax.fill_between([V.tensor[i][0], V.tensor[i][4]], [V.tensor[i][5], V.tensor[i][5]], [V.tensor[i][1], V.tensor[i][1]], alpha = alpha, color = color)
            
            ax.set_xlim(par_bound[0][0], par_bound[0][1])
            ax.set_xlabel(r'$\varepsilon_1$')
            ax.set_ylim(par_bound[1][0], par_bound[1][1])
            ax.set_ylabel(r'$\varepsilon_2$')
            
            
    elif len(par_bound) == 3:
        
        for i in range(len(V.tensor)):
            if  V.tensor[i][-1] == 'undef': #undefined: part of the parameter space that is not studied
                color = 'k'
                alpha = 1
                
            elif float(V.tensor[i][-1]) < 0. : # not satisfied
                color = given_color #'b'
                alpha = 0 
            elif float(V.tensor[i][-1]) > 0. : # satisfied 
                alpha = given_alpha 
                color = given_color #'b'
            elif float(V.tensor[i][-1]) == 0.:  # grey situation 
                alpha = 0 
                color = 'grey'
            
          
            poly = CreatePoly(V.tensor[i], alpha, color)
            ax.add_collection3d(poly, zdir = 'z')
            
            
        ax.set_xlim(par_bound[0][0], par_bound[0][1])
        ax.set_xlabel(r'$\varepsilon_1$')
        ax.set_ylim(par_bound[1][0], par_bound[1][1])
        ax.set_ylabel(r'$\varepsilon_2$')
        ax.set_zlim(par_bound[2][0], par_bound[2][1])     
        ax.set_zlabel(r'$\varepsilon_3$')
    return ax

   
def PlotQuant(V1, V2, ax, mode):   
    
 MM = -10000000
 mm =  1000000
    
 if mode =='A':   
     for i in range(len(V1.tensor)):
          if abs( float(V1.tensor[i][-1])  - float( V2.tensor[i][-1]) ) < mm: 
              mm = abs( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) )
          if abs( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) ) > MM:  
              MM = abs( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) )
      
     for i in range(len(V1.tensor)):
        if float(V1.tensor[i][-1] < 0.) and float(V2.tensor[i][-1] < 0.): # both not satisfied
            color = 'tomato'
            alpha = 0.5
            cmap=plt.cm.viridis
            ax.fill_between([V1.tensor[i][0], V1.tensor[i][2]], [V1.tensor[i][3], V1.tensor[i][3]], [V1.tensor[i][1], V1.tensor[i][1]], 
                        alpha = alpha,  color =color)
            
        elif float(V1.tensor[i][-1] > 0.) and float(V2.tensor[i][-1] > 0.): # both satisfied 
            alpha = 0.5
            color = 'palegreen'
            cmap=plt.cm.viridis
            ax.fill_between([V1.tensor[i][0], V1.tensor[i][2]], [V1.tensor[i][3], V1.tensor[i][3]], [V1.tensor[i][1], V1.tensor[i][1]], 
                        alpha = alpha,  color =color)
        else:
            alpha = 1
            # 1--> white, 0--> black
            #color = str( 1 - ((abs( V1.tensor[i][4]  - V2.tensor[i][4] ) - mm )/(MM - mm) ))
            
            norm = mpl.colors.Normalize(vmin=mm, vmax=MM)
            cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Blues)
            cmap.set_array([])  
                        
            ax.fill_between([V1.tensor[i][0], V1.tensor[i][2]], [V1.tensor[i][3], V1.tensor[i][3]], [V1.tensor[i][1], V1.tensor[i][1]], 
                        alpha = alpha,  color =cmap.to_rgba(abs( V1.tensor[i][4]  - V2.tensor[i][4]))) #cmap = 'Blues' , color = color)
        
        
 elif mode =='B':    
         for i in range(len(V2.tensor)):
           if ( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) ) < mm:  
                      mm = abs( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) )
           if ( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) ) > MM:  
                      MM = abs( float(V1.tensor[i][-1])  - float(V2.tensor[i][-1]) )
        
         for i in range(len(V2.tensor)):
            if float(V1.tensor[i][-1] < 0.) :
                color = 'tomato'
                alpha = 0.5
            elif float(V1.tensor[i][-1] > 0.) and float(V2.tensor[i][-1] > 0.): # both satisfied 
                alpha = 0.5
                color = 'palegreen'
            else:
                alpha = 1
                color = str( 1 - ((( V1.tensor[i][-1]  - V2.tensor[i][-1] ) - mm )/(MM - mm) ))
            ax.fill_between([V1.tensor[i][0], V1.tensor[i][2]], [V1.tensor[i][3], V1.tensor[i][3]], [V1.tensor[i][1], V1.tensor[i][1]], 
                    alpha = alpha, color = color )
 return ax



def plot_validity_domains(par_bound, V1, V2,  parameters, bool_quantitative, V3 ):
    if not bool_quantitative:
        fig, ax = plt.subplots(1, 1, figsize=(25, 30))#(30, 30))#(30,8))#(15, 30)) #(20,30)
        ax = PlotVals_2or3dim(par_bound, V1, ax,  'aqua' , 0.5)
        ax = PlotVals_2or3dim(par_bound, V2, ax,   'darkred', 0.4)  
        if V3 is not None: ax = PlotVals_2or3dim(par_bound, V3, ax,   'sandybrown', 0.4)  

    elif bool_quantitative:
        
        mode = 'A'
        
        if mode == 'B':
            fig, [ax1,ax2] = plt.subplots(2, 1, figsize=(20,30))
            ax1 = PlotQuant(V1, V2, ax1, mode )
            ax2 = PlotQuant(V2, V1, ax2, mode )
        
        else: 
            fig, ax = plt.subplots(1, 1, figsize=(30,30)) #(15, 30 #(30,8)
            if V3 is None: ax = PlotQuant(V1, V2, ax, mode )
            
        
    ax.scatter(parameters[0][0],parameters[0][1], s= 1000 , color = 'black', label = '$\hat{p}_1$') #color = 'green'
    # ax.scatter(parameters[1][0],parameters[1][1], s= 400 , color = 'green', label = '$\hat{p}_2$') #color = 'indigo' fuchsia
    if V3 is not None: ax.scatter(parameters[2][0],parameters[2][1], s= 300 , color = 'yellow', label = '$\hat{v}_3$') #color = 'yellow'
    
    # ax.legend(fontsize = 60)
    
    # ax.set_xlabel('T') #'T'
    # ax.set_ylabel('p') # 'p'
    
    # plt.xlabel(r'$\varepsilon_1$', fontsize = 50)    
    # plt.ylabel(r'$\varepsilon_2$', fontsize = 50) 
    
    # plt.xlabel(r'$T$', fontsize = 80)    
    # plt.ylabel(r'$p$', fontsize = 80) 
    
    # plt.xlabel(r'$T_1$', fontsize = 80)    
    # plt.ylabel(r'$T_2$', fontsize = 80) 
    
    plt.xlabel(r'$v_{no-crash}$', fontsize = 120)    
    plt.ylabel(r'$d_{no-crash}$', fontsize = 120) 
    
    # plt.xlabel(r'$v_{crash}$', fontsize = 120)    
    # plt.ylabel(r'$d_{crash}$', fontsize = 120) 
    
    plt.xticks(fontsize=90)    
    plt.yticks(fontsize=90) 
    # plt.xlim(left = 8)#(left = 0, right = 550)
    plt.xlim( right = 10.3)##550)
    # plt.ylim( bottom =0.9, top = 1.7)
    # plt.xlim( left = 8)
    # plt.ylim( bottom =0.9, top = 1.7)
    plt.legend(loc ='upper right', fontsize = 120)
    # plt.locator_params(axis='x', nbins=4)
    # plt.locator_params(axis='y', nbins=5)
    if os.path.exists(f"plot_val_domain_par{parameters}.pdf"): plt.savefig(f"plot_2nd_val_domain_par{parameters}.pdf", format='pdf', bbox_inches="tight")      
    else:  plt.savefig(f"plot_val_domain_par{parameters}.pdf", format='pdf', bbox_inches="tight") 
        
    return
 
        
    ##Plot the validity domains only in case the parameter space is 2 or 3 dimensional
    # if len(par_bounds)==2  or  len(par_bounds)==3: 
        
    #     if len(par_bounds)==2: fig, [ax0, ax1] = plt.subplots(2, 1, figsize=(20,30))
        
    #     elif len(par_bounds)==3: 
    #         fig = plt.figure(figsize=(20,30))
    #         ax0 = fig.add_subplot(1, 2, 1, projection='3d')
    #         ax1 = fig.add_subplot(1, 2, 2, projection='3d')
            
    #     ax0.set_title('Class = 1' )
    #     ax0 = fun_p.PlotVal(V1, ax0, par_bounds)
    #     ax1.set_title('Class = 2' )
    #     ax1 = fun_p.PlotVal(V2, ax1, par_bounds)
        
    # ##Plots for parameter space 2 or 3 dimensional
    # if len(par_bounds)==2: 
    #     #Validity domain class 1:
    #     ax0.plot(parameters[0][0],parameters[0][1], 'ro') #point in class 1
    #     ax0.plot(parameters[1][0],parameters[1][1], 'go') #point in class 2
        
    #     #Validity domain class 2:
    #     ax1.plot(parameters[0][0],parameters[0][1], 'ro') #point in class 1
    #     ax1.plot(parameters[1][0],parameters[1][1], 'go') #point in class 2
    
    # elif len(par_bounds)==3: 
    #     # validity domain class 1:
    #     ax0.scatter(parameters[0][0],parameters[0][1], parameters[0][2], 'ro') #point in class 1
    #     ax0.scatter(parameters[1][0],parameters[1][1], parameters[1][2], 'go') #point in class 2
    #     # validity domain class 2:
    #     ax1.scatter(parameters[0][0],parameters[0][1], parameters[0][2], 'ro') #point in class 1
    #     ax1.scatter(parameters[1][0],parameters[1][1], parameters[1][2], 'go') #point in class 2
    
