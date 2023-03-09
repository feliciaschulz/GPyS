# -*- coding: utf-8 -*-
"""
Implementation of the R code GPS.r in Python

Felicia Schulz

GPS.r script and data (data.csv, gen.csv, geo.csv) acquired from:
    https://github.com/homologus/GPS/tree/master/GPS-original-code
"""

import os
import pandas as pd
import scipy as sp
import numpy as np

# have to be in directory where the data is 

def GPS(outfile_name='my_GPS_results.txt', N_best=10, filename="data.csv"):
    
    # load the data
    GEO = pd.read_csv("geo.csv", header=0, index_col=0)
    GEN = pd.read_csv("gen.csv", header=None, index_col=0)
    TRAINING_DATA = pd.read_csv(filename, header=0, index_col=0)
    
    # create distance matrices x and y from geo and gen
    y = sp.spatial.distance.pdist(GEO)
    x = sp.spatial.distance.pdist(GEN)
    
    # loop through matrices, if geographical distance is >=70 or genetic distance
    # is >=0.8, both are 0
    LL = len(y)
    for l in range(LL):
        if y[l] >= 70 or x[l] >= 0.8:
            y[l] = 0
            x[l] = 0
            
    # make the linear regression, we will only need the slope for later        
    slope, intercept, r, p, std_err = sp.stats.linregress(x, y)      
    
    # make the groups variable: array with all unique populations
    groups = TRAINING_DATA["GROUP_ID"].unique()
    
    # write header to output
    with open(outfile_name, "w") as f:
        f.write("Population\tSample_no\tSample_id\tPrediction\tLat\tLon\n")
        
    # not sure what N_best is for
    N_best = min(N_best, len(GEO))
    
    
    for group in groups:
        training_data_subset = TRAINING_DATA[TRAINING_DATA["GROUP_ID"] == group] # training_data_subset=Y
        num_rows = len(training_data_subset) # num_rows=K -> number of rows in subset
        
        # loop through rows
        for row in range(num_rows): # row=a
            current_row_df = training_data_subset.iloc[row, :9].values # current_row_df=X
            E_vector = np.zeros(len(GEO)) # E_vector=E; zero vector with len=len(GEO)
            
            # initialise variables that are for ???
            minE = 10000
            minG = -1
            minG_2 = -1
            
            # loop through rows in GEO
            for geo_population in range(len(GEO)): # geo_population=g
                ethnic = GEO.index[geo_population] # current ethnic group
                gene = GEN.loc[ethnic, :9].values # current genetic markers for current ethnic group
                # add value for each population in E, this represents the genetic marker values as a vector
                #   in some way compared to the gen data
                E_vector[geo_population] = np.sqrt(np.sum((gene - current_row_df) ** 2))
            
            # minE = smaller version of E_vector, with 10 smallest numbers
            minE = np.sort(E_vector)[0:N_best]
            # minG = zero vector with N_best number of values
            minG = np.zeros(N_best, dtype=int)
            
            for geo_populations_2 in range(len(GEO)): #geo_populations_2=g
                for n in range(N_best): # n=j
                 
                    """The R code uses the function all.equal() here, which returns TRUE if 
                    two items are not identical but similar enough. Instead, here, np.allclose() will
                    be used, but the tolerance must be the same as the one used by all.equal() by default
                    The default value listed by rdocumentation.org is "close to 1.5e-8"."""
                
                    if np.allclose(minE[n], E_vector[geo_populations_2], rtol=1.5e-8):
                        minG[n] = geo_populations_2
                        # (?) minG has all of the indexes of the populations in GEO for which this
                        #   specific sample has the 10 smallest genetic distances
                        
            radius = E_vector[minG] # this has all of the 10 lowest genetic distance calculations
            best_ethnic = GEO.index[minG] # these are the 10 closest ethnic groups
            radius_geo = slope*radius[0]
            
            
            # I don't know what W is
            print(minE)
            try:
                W = (minE[0]/minE)**4
                W = W/sum(W)
            except:
                print(minE)
            
            delta_lat = GEO.iloc[minG, 0].values - GEO.iloc[minG[0], 0]
            delta_lon = GEO.iloc[minG, 1].values - GEO.iloc[minG[0], 1]
            
            new_lat = sum(W*delta_lat)
            new_lon = sum(W*delta_lon)
            
            lo1 = new_lon * min(1, radius_geo / np.sqrt(new_lon ** 2 + new_lat ** 2))
            la1 = new_lat * min(1, radius_geo / np.sqrt(new_lon ** 2 + new_lat ** 2))
            
            
            with open(outfile_name, "a") as f:
                f.write(f"{group}\t{row+1}\t{training_data_subset.index[row]}\t{best_ethnic[0]}\t{GEO.iloc[minG[0], 0]+la1}\t{GEO.iloc[minG[0], 1]+lo1}")

            
GPS()
            
            





















