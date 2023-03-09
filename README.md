# PopGen_Project

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











