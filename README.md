# GPyS (Population Genetics Project)

GPyS is a python implementation and web application of the Geographic Population Structure (GPS) algorithm (Elhaik et al., 2014).  
With GPS, individuals' ancestral population as well as latitude and longitude of origin can be predicted from genetic admixture data.

The GPyS application as well as GPS.py were created by Felicia Schulz in March 2023.

## The GPS algorithm and data
The original GPS algorithm was written in R by Elhaik et al. (2014) and the research paper can be found here: https://www.nature.com/articles/ncomms4513  
The original GPS.r code and the data as well as explanations about how to create the input data for GPyS can be found here:  
https://github.com/homologus/GPS.

## Purpose of GPyS
This project had the aim of translating the original GPS R code into python and creating a web application in order to facilitate the use of GPS.

## How to use GPyS

### Softwares and versions
GPyS was created in Python (v. 3.10.8). The library Streamlit (v. 1.19.0) was used to create the web application. Other necessary dependencies are numpy (v 1.24.2), pandas (v. 1.5.3), scipy (1.10.1) and plotly (v. 2.18.1).


The easiest way to install streamlit which will work in most cases is by simply using pip in the command line.
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
Once you have successfully navigated to the web application, you will see a prompt for uploading your input data. GPyS needs three input data files:
1. GEN.csv
2. GEO.csv
3. Your sample data.csv file.   

All three files should be in .csv format, as seen in https://github.com/homologus/GPS. The input files do not need to be in the same directory as GPyS.py.

Please make sure to upload the correct files in each of the "Upload file" boxes. If they are in the wrong order, the algorithm will not work.

Next, you have to specify how what you want N_best to be. This is a variable required by the GPS algorithm which determines out of how many of the closest Euclidean distance values the geographical radius will later be computed. For more information on this, see https://www.nature.com/articles/ncomms4513. If you are unsure about which value to choose, a good default is 10. Press enter to start the GPS algorithm.

Please make sure to only enter a number and no other symbols, otherwise it will not work.

### GPS algorithm and output

Once all of the input files and variables are entered, the GPS algorithm will run. This may take a while depending on how large the data is. With the sample data found in 01_OriginalCode/GPS_Data in this repository, this will take around thirty seconds.

When the computation is finished, you will see a green message declaring that it is done. The output data file is automatically saved to your current working directory with the name "my_GPyS_results.txt". An example output file can also be found in 1_OriginalCode/GPS_Data and 3_GPyS.  Now, you can inspect your data in GPyS as well.

### Output visualization
Your output data file is displayed as a table and as an interactive map. You can enlarge both with the buttons on the top right of each.

In the table, you can see your output data file and scroll through. On the map, the individual data points represent each individual. The map was constructed by using the latitude and longitude data predicted by the GPS algorithm.

Pay attention to the bar on the top right of the map as there are further options such as zooming, marking areas on the map and saving the map as an image to your current working directory.

## Repository structure
Finally, some explanations about the structure of this repository:
- 0_Documentation contains this README again, the power point presentation for this project, a .py file with pseudocode which I wrote for gaining a better understanding of GPS.r, and the research paper for GPyS.
- 1_OriginalRCode contains the original GPS.r algorithm as found in https://github.com/homologus/GPS. Within this directory, there is also the GPS data used by Elhaik et al. (2014), which was the example data for this project.
- 2_GPSPython contains the pure GPS algorithm written in python, translated from GPS.r. There is no web application.
- 3_GPyS contains the final GPyS.py code as well as an example output.










