#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pseudocode for GPS.py

This file is for understanding the GPS.r code.

Implementation of the R code GPS.r in Python

Steps:
    - Load data: GEO.csv, GEN.csv, data.csv
    - Create distance matrices of x=gen.csv and y=geo.csv
    - Loop through x and y; if the geographical distance between two
        is >=70 or the genetic distance is >= 0.8, make them 0 in both matrices
    
    - Fit a linear model to x and y

    - Have a GROUPS variable which is a set of all of the unique data.csv populations
    
    - Write header to output file
    
    - Have variable N_best ???? the smaller value of the number of GEO rows and 10
        (in this case 10 is smaller, nrows(GEO) is 143)
        
        
    - Loop through GROUPS
    - Create variable Y = a subset of data.csv where group_id is the current one being
        looped through
    - Create variable K = the number of rows of Y, aka the number of samples where
        the group is the current one being looped through
     
        - Loop through 1:K (aka through the rows in Y)
        - Create X = data frame that is the current row in Y, but only columns 1:9,
            so not the one with group_id
        - Create E = zero vector, has as many 0s as there are rows in GEO
        - Create variables minE, minG, second_minG (?)

            - Loop through rows in GEO (143)
            - Create variable ethnic = current ethnic group
            - Create variable gene = current genetic markers for current ethnic group
            - Add the genetic marker information to the vector E at position g:
                sqrt of sum of squares of gene info - X
                -> so I think it's like, for this individual, this is the genetic marker information
            
            
---Not finished---

"""

