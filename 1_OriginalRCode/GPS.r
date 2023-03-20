 GPS<-function(outfile_name='GPS_results.txt',N_best=10, fname="data.csv", directory_name="~/Documents/Uni/LundUniversity/BINP29/Project/1_OriginalCode/GPS"){

 setwd(directory_name)    #set directory
 GEO=read.csv("geo.csv", header=TRUE,row.names=1)
 GEO=GEO[,1:2]
 GEN=(read.csv("gen.csv", header=FALSE,row.names=1))  #as.numeric
 TRAINING_DATA=read.csv(fname, header=TRUE, row.names=1)
 y=dist(GEO)
 x=dist(GEN)
          
 LL=length(y)
 for(l in 1:LL){
    if(y[l]>=70 || x[l] >=0.8) {y[l]=0; x[l]=0;}
 }
 
 eq1<-lm(y~x);              
 
 GROUPS=unique(TRAINING_DATA$GROUP)
 
 write("Population\tSample_no\tSample_id\tPrediction\tLat\tLon",outfile_name, append=FALSE)
 
 N_best<-min(N_best,length(GEO[,1]))
 
 for(GROUP in GROUPS){
 Y=subset( TRAINING_DATA, TRAINING_DATA$GROUP_ID==GROUP) 
 K=length(Y[,1])
       for(a in 1:K){        
         X<-Y[a,1:9]
         E<-rep(0, length(GEO[,1])  )  ;
         minE=10000; minG=-1; second_minG=-1;
         for(g  in 1: length(GEO[,1])){
            ethnic<-attributes(GEO[g,])$row.names;
            gene<-as.numeric(GEN[ethnic,1:9])
            E[g]<-   sqrt(sum((gene-X)^2))
            }
          minE=c();minE<-c(minE,sort(E,FALSE)[1:N_best])
          minG=c();
          for(g  in 1: length(GEO[,1])){
            for(j in 1:N_best){
              if( isTRUE(all.equal(minE[j], E[g]))){minG[j]=g;} 
              }
            }
            
          minG; 
          radius<-E[minG]; 
          best_ethnic<- attributes(GEO[minG,])$row.names; #best_ethnic;
          radius_geo=(eq1[[1]][2]*radius[1])
          W<- (minE[1]/minE)^4;
          W=W/(sum(W));
          delta_lat<-(GEO[minG,][[1]]-GEO[minG[1],][[1]])
          delta_lon<-(GEO[minG,][[2]]-GEO[minG[1],][[2]])
          new_lon<-sum(W*delta_lon)
          new_lat<-sum(W*delta_lat)
          lo1<-new_lon*min(1,radius_geo/sqrt(new_lon^2+new_lat^2) )
          la1<-new_lat*min(1,radius_geo/sqrt(new_lon^2+new_lat^2))
          write(paste(GROUP, a, row.names(Y[a,]), best_ethnic[1],GEO[minG[1],1]+la1,GEO[minG[1],2]+lo1, sep="\t"),outfile_name, append=TRUE)
        }
   }
 return ("Done!");
 }
 
GPS()

