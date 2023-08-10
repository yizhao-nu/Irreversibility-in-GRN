library(BoolNet)
library(dplyr)
fp = commandArgs()[6]
print(fp)

fp_rs2 = paste('/data/yizhao/irr_grn/netfiles/', fp,'.net',sep='')
fp_unique = paste('/data/yizhao/irr_grn/attfiles/','1st',fp,".csv",sep='')
unique <- read.csv(fp_unique,header=FALSE)
unique = apply(unique, 2, function(r) paste(r))
print(dim(unique))

fp_result_KO = paste('/data/yizhao/irr_grn/results/result','KO',fp,'pre','.csv',sep='-')
fp_result_OE = paste('/data/yizhao/irr_grn/results/result','OE',fp,'pre','.csv',sep='-')

fp_changed = paste('/data/yizhao/irr_grn/results/changed','pre',fp,'.csv',sep='-')
rs2 <- loadNetwork(fp_rs2)

alterState <- function(S,i){
    #print(S[i])
    #S = lapply(S,as.numeric)
    #print(S[i])
    S[i] <- 1- S[i]
    
    return(S)
}



not_in_attractors <- function(atts,a){
    num_atts = dim(atts)[1]
    atts[num_atts+1,] = lapply(a,as.numeric)
    atts2 <- distinct(atts)
    num_atts2 <- dim(atts2)[1]
   
    if (num_atts == num_atts2){
        c <- 0
    
    } else {
        c <- 1
    }
    
    return(c)
}
changed <- function(atts,a){
    changed <- 0
    if (not_in_attractors(atts,a)==1){
        for (i in 1:dim(atts)[1]){
            changed <- changed + sum(abs(atts[i,]-lapply(a,as.numeric)))/dim(atts)[1]

            }
    }
    
    return(changed)
}

net <- rs2
num_nodes = 87
start = unique
epochs = dim(start)[1]
print(epochs)
results_KO <- matrix(NA,epochs+2,num_nodes)
results_OE <- matrix(NA,epochs+2,num_nodes)
rec <- matrix(NA,epochs,num_nodes)

num_changed <- matrix(NA,epochs+1,num_nodes)
ones <- 0 
skipped <- 0
#A_prev <- matrix(0,2,876)

####### use found attractors #######
for (j in 1:dim(start)[1]){
    
    IS <- as.numeric(unlist(start[j,]))
       print(IS)
    
    
   
    p0 <- getPathToAttractor(net,IS)
    print(p0)
    
    A0 <- p0[attr(p0,'attractor'):dim(p0)[1],]
    S0 <- A0[1,]


    s=Sys.time()
    
    for (i in 1:num_nodes){
    
        
        
        if(S0[i]==1){
            
            S1 <- alterState(S0,i)
            new_i = S1[i]
            
            N1 <- fixGenes(net,i,new_i)
            #print(N1)
            p1 <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'first'))
            
            
            A1 <- lapply(p1[dim(p1)[1],],as.numeric)
            
            N2 <- fixGenes(N1,i,-1)

            #S2 <- alterState(A1,i)
            A1[i] = 1 - new_i
            #print(A1)
            #S2 <- A1
            p2 <- getPathToAttractor(N2,A1,includeAttractorStates = 'first')
            A2 <- p2[dim(p2)[1],]
            

            IRR <- not_in_attractors(A0,A2)
            ones = ones + IRR

            results_KO[j,i] <- IRR
            results_OE[j,i] <- NA
            num_changed[j,i] <- changed(A0,A2)
            rec[j,i] <- 1
        
        }
        else if(S0[i]==0){
            
            S1 <- alterState(S0,i)
            new_i = S1[i]
            
            N1 <- fixGenes(net,i,new_i)
            #print(N1)
            #try(
            p1 <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'first'))
            
            A1 <- lapply(p1[dim(p1)[1],],as.numeric)
            
            N2 <- fixGenes(N1,i,-1)

            #S2 <- alterState(A1,i)
            A1[i] = 1 - new_i
            #print(A1)
            #S2 <- A1
            p2 <- getPathToAttractor(N2,A1,includeAttractorStates = 'first')
            A2 <- p2[dim(p2)[1],]
            

            IRR <- not_in_attractors(A0,A2)
            
            ones = ones + IRR

            results_OE[j,i] <- IRR
            results_KO[j,i] <- NA
            num_changed[j,i] <- changed(A0,A2)
            rec[j,i] <- 0
        
        }
    }
    
    e=Sys.time()
    print(e-s)
    
    

}

colnames(results_OE) <- names(p1)
colnames(results_KO) <- names(p1)

results_OE[epochs+1,] = colMeans(results_OE, na.rm=T)
results_OE[epochs+2,] = 1- (colSums(rec, na.rm=T)/(epochs-skipped))
results_OE <- results_OE[,order(results_OE[epochs+1,],decreasing=TRUE)]
write.csv(results_OE,fp_result_OE)

results_KO[epochs+1,] = colMeans(results_KO, na.rm=T)
results_KO[epochs+2,] = colSums(rec, na.rm=T)/(epochs-skipped)
results_KO <- results_KO[,order(results_KO[epochs+1,],decreasing=TRUE)]
write.csv(results_KO,fp_result_KO)


colnames(num_changed) <- names(p1)
num_changed[epochs+1,] = colSums(num_changed)/(epochs-skipped)
num_changed <- num_changed[,order(num_changed[epochs+1,],decreasing=TRUE)]
write.csv(num_changed,fp_changed)






    





