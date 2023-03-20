#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPyS algorithm and web application implementation
Felicia Schulz
"""

import streamlit as st
import pandas as pd
import scipy as sp
import numpy as np
import plotly.express as px

finished = False
failed = False

st.markdown("<h1 style='text-align: center; '>GPyS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; '>Geographic Population Structure algorithm in Python</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; '>Created by Felicia Schulz</p>", unsafe_allow_html=True)



st.write("Please upload your input data and specify your N_best.")

data = st.file_uploader("Upload your data file.", type="csv", help="Use your GPS file" )
gen = st.file_uploader("Upload your gen.csv file.", type="csv", help="Use your GPS file" )
geo = st.file_uploader("Upload your geo.csv file.", type="csv", help="Use your GPS file" )
N_best = st.text_input("Please specify N_best (enter an integer)")
# Error-proofing N_best
if len(N_best) > 0:
    try:
        N_best = int(N_best)
    except:
        st.write("N_best must be a number. Please do not write any non-numerical characters. Reload the page to try again.")
        N_best = None



def GPyS(outfile_name='my_GPyS_results.txt', N_best=10):
    
    # load the data
    GEO = pd.read_csv(geo, header=0, index_col=0)
    GEN = pd.read_csv(gen, header=None, index_col=0)
    TRAINING_DATA = pd.read_csv(data, header=0, index_col=0)
    
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
        f.write("Population\tSample_no\tSample_id\tPrediction\tlat\tlon\n")
        
    # not sure what N_best is for
    N_best = min(N_best, len(GEO))
    
    
    for group in groups:
        training_data_subset = TRAINING_DATA[TRAINING_DATA["GROUP_ID"] == group] # training_data_subset=Y
        num_rows = len(training_data_subset) # num_rows=K -> number of rows in subset
        
        # loop through rows in your subset group data
        for row in range(num_rows): # row=a
            current_row_df = training_data_subset.iloc[row, :9].values # current_row_df=X
            E_vector = np.zeros(len(GEO)) # E_vector=E; zero vector with len=len(GEO)
            
            # initialise variables
            minE = 10000
            minG = -1
            
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
                 
                    #The R code uses the function all.equal() here, which returns TRUE if 
                    #two items are not identical but similar enough. Instead, here, np.allclose() will
                    #be used, but the tolerance must be the same as the one used by all.equal() by default
                    #The default value listed by rdocumentation.org is "close to 1.5e-8".
                
                    if np.allclose(minE[n], E_vector[geo_populations_2], rtol=1.5e-8):
                        minG[n] = geo_populations_2
                        # minG has all of the indexes of the populations in GEO for which this
                        # specific sample has the 10 smallest genetic distances
                        
            radius = E_vector[minG] # this has all of the 10 lowest genetic distance calculations
            best_ethnic = GEO.index[minG] # these are the 10 closest ethnic groups
            radius_geo = slope*radius[0]
            

            W = (minE[0]/minE)**4
            W = W/sum(W)
            
            delta_lat = GEO.iloc[minG, 0].values - GEO.iloc[minG[0], 0]
            delta_lon = GEO.iloc[minG, 1].values - GEO.iloc[minG[0], 1]
            
            new_lat = sum(W*delta_lat)
            new_lon = sum(W*delta_lon)
            
            lo1 = new_lon * min(1, radius_geo / np.sqrt(new_lon ** 2 + new_lat ** 2))
            la1 = new_lat * min(1, radius_geo / np.sqrt(new_lon ** 2 + new_lat ** 2))
            
            
            with open(outfile_name, "a") as f:
                f.write(f"{group}\t{row+1}\t{training_data_subset.index[row]}\t{best_ethnic[0]}\t{GEO.iloc[minG[0], 0]+la1}\t{GEO.iloc[minG[0], 1]+lo1}\n")


# check if all the input exists before running GPS function
if data is not None and geo is not None and gen is not None and isinstance(N_best, int):
    # loading spinner
    with st.spinner('Computing the GPS Analysis...'):
        try:
            GPyS(N_best=N_best)
        except:
            st.write("Something went wrong. Please check if your input files are correct. Reload the page to try again.")
            failed = True
    if failed == False:
        st.success('Done! Your results file has been saved to your current working directory.')
        finished = True




if finished == True:
    
    # if it exists, open the results file which shoudl be in the same folder
    with open("my_GPyS_results.txt", "r") as results:
        df_results = pd.read_csv(results, sep="\t", header=0) # load as pandas data frame
    st.dataframe(df_results, use_container_width=True)
    
    
    
    # calculate the percentage of individuals predicted to come from their region of origin
    total_wrong = 0
    # loop through the results df
    for index, row in df_results.iterrows():
        pop = row["Population"]
        predicted = row["Prediction"]
        # the block of code below changes the predicted string so that they are comparable
        predictedlist = predicted.split("_")
        if len(predictedlist) <= 2:
            predicted = predictedlist[0]
        elif len(predictedlist) > 2:
            predicted = ""
            for word in range(len(predictedlist)-1):
                predicted += "_"
                predicted += predictedlist[word]
            predicted = predicted[1:]
        
        # compare predicted and actual population origin
        if pop != predicted:
            total_wrong += 1
            
    # calculate percentage and print to screen
    percentage_right = (index-total_wrong)/index
    st.write("Percentage of individuals predicted to come from their region of origin:", percentage_right, "%")


    # now remove na values for the mapping plot
    df_results = df_results.dropna()
    
    # plot the results using plotly
    fig = px.scatter_geo(df_results,
                        lat=df_results["lat"],
                        lon=df_results["lon"],
                        hover_name="Sample_id",
                        hover_data=["Population", "Prediction"])

    st.plotly_chart(fig)












