# GPyS

GPyS is a python implementation and web application of the Geographic Population Structure (GPS) algorithm.  
With GPS, individuals' ancestral population as well as latitude and longitude of origin can be predicted from genetic admixture data.

## The GPS algorithm and data
The original GPS algorithm was written in R by Elhaik et al. (2014) and the research paper can be found here: https://www.nature.com/articles/ncomms4513  
The original GPS.r code and the data as well as explanations about how to create the input data for GPyS can be found at https://github.com/homologus/GPS.

## Purpose of GPyS
This project had the aim of translating the original GPS R code into python and create a web application in order to facilitate the use of GPS.

## How to use GPyS

### Softwares and versions
GPyS was created in Python (v. 3.10.8). The library Streamlit (v. 1.19.0) was used to create the web application. Other necessary dependencies are numpy (v 1.24.2), pandas (v. 1.5.3), scipy (1.10.1) and plotly (2.18.1).


The easiest way to install streamlit which will work in most cases is simply using pip in the command line.
```bash
pip install streamlit
```
However, depending on the operating system, some alternative ways may be better. In that case, more information and instructions for installing streamlit can be found here:  
 https://docs.streamlit.io/library/get-started/installation


### Running GPyS
After having installed all necessary libraries and dependencies, streamlit can be run straight from the command line. First, open the terminal and navigate to the directory in which you have stored GPyS.py. Then, run the application.
```bash
cd ~/example_directory_name/
streamlit run GPyS.py
```
This command will open the GPyS web application automatically in the default browser.

## The GPyS web application

### User input
Once you have successfully navigated to the web application, you will see a prompt for uploading your input data.  
GPyS needs three input data files:
1. GEN.csv
2. GEO.csv
3. Your sample data.csv file.   

All three files should be in .csv format, as specified in https://github.com/homologus/GPS. The input files do not need to be in the same directory as GPyS.py.

Please make sure to upload the correct files in each of the "Upload file" boxes. If they are in the wrong order, the algorithm will not work.

Next, you have to specify how what you want N_best to be. This is a variable required by the GPS algorithm which determines out of how many of the closest Euclidean distance values the geographical radius will later be computed. For more information on this, see https://www.nature.com/articles/ncomms4513. If you are unsure which value to choose, a good default is 10. Press enter to start the GPS algorithm.

Please make sure to only enter a number and no other symbols, otherwise it will not work.

### GPS algorithm and output

Once all of the input files and variables are entered, the GPS algorithm will run. This may take a while depending on how large the data is. With the sample data found in 01_OriginalCode/GPS_Data in this repository, this will take around thirty seconds.

When the computation is finished, you will see a green message declaring that it is done. The output data file is automatically saved to your current working directory with the name "my_GPS_results.txt". An example output file can also be found in    Now, you can inspect your data in GPyS as well.

### Output visualization
Your output data file is displayed as a table and as an interactive map. You can enlarge both with the buttons on the top right of each.

In the table, you can see your 




## Understanding the code and data
- GEN.csv = the genetic signature of each of the reference populations
- GEO.csv = the geographical coordinates of each of the reference populations
- data.csv = the input data set with all of the participants whose genetic geographical origin is to be tested

In order to make the R code work, one line had to be slightly altered in order to load the data correctly.

```R
# original line:
GEN=(read.csv("gen.csv", header=TRUE,row.names=1)) 
# altered line:
GEN=(read.csv("gen.csv", header=FALSE,row.names=1)) 
```



```bash
streamlit run GPyS.py
```







