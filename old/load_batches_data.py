# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 18:14:05 2017

@author: Karolis
"""

from scipy.io import loadmat
       

def load_batches_data(path_to_mat):
    '''
        Extracts data from a .mat file and returns an array of dictionaries 
        where each dictionary represents a batch.
        
        Input:
            path_to_mat (string) - path to .mat file
    '''
    mat = loadmat(path_to_mat)
    key = [key for key in mat.keys() if "__" not in key][0]
    batches = []
    
    for batch in [batch[0][0] for batch in mat[key][0][0]]:
        try:
            batches.append({})
            
            for variable in batch:
                # Creates a key (variable name) - value pair
                batches[-1][variable[0][0][0][0]] = dict(
                                                y_unit=variable[0][0][1][0],
                                                t_unit=variable[0][0][2][0],
                                                t=variable[0][0][3],
                                                y=variable[0][0][4],
                                                )
        except BaseException as e:
            if batches[-1] == {}:
                del batches[-1]
    
    return batches        


#batches = load_batches_data("combined_batches_data.mat")
 


        