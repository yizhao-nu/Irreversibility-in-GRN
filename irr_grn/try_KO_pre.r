library(BoolNet)
library(dplyr)
fp = commandArgs()[6]
print(fp)

fp_rs2 = paste('./netfiles/', fp,'.net',sep='')
fp_unique = paste('./attfiles/','1st_',fp,".csv",sep='')
unique <- read.csv(fp_unique,header=FALSE)
print(dim(unique))
epochs = min(dim(unique)[1],15000)
start = apply(unique, 2, function(r){ paste(r)}) ## converts to character

              

fp_result_KO = paste('./results/result-KO-',fp,'-pre.csv',sep='')
fp_result_OE = paste('./results/result-OE-',fp,'-pre.csv',sep='')
fp_changed = paste('./results/changed-pre-',fp,'.csv',sep='')
net <- loadNetwork(fp_rs2)

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

num_nodes = 87
epochs = min(dim(start)[1],15000)
print(epochs)
results_KO <- matrix(NA,epochs+2,num_nodes)
results_OE <- matrix(NA,epochs+2,num_nodes)
rec <- matrix(NA,epochs,num_nodes)

num_changed <- matrix(NA,epochs+1,num_nodes)
ones <- 0  ##  counter for the attractors
skipped <- 0 ## is this needed ?


####### use found attractors #######
for (j in 1:epochs){ 
    IS <- as.numeric(unlist(start[j,]))
    ## print(IS)
    
    ## get periodic attractor
    p0 <- try(getPathToAttractor(net,IS))
    if (inherits(p0)=='try-error'){ next }
    ## print(p0)
    A0 <- p0[attr(p0,'attractor'),]
    S0 <- A0[1,]
    s=Sys.time()
    
    for (i in 1:num_nodes){
        S1 <- alterState(S0,i)
        new_i = S1[i]
        N1 <- fixGenes(net,i,new_i)
        p1 <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'first'))
        if(inherits(p1, "try-error")){
            results_OE[j,i] <- NA
            results_KO[j,i] <- NA
            num_changed[j,i] <- 0        
            next
        }
        A1 <- lapply(p1[dim(p1)[1],],as.numeric)
        N2 <- fixGenes(N1,i,-1)
        A1[i] = 1 - new_i
        p2 <- try(getPathToAttractor(N2,A1,includeAttractorStates = 'first'))
        if(inherits(p2, "try-error")){
            results_OE[j,i] <- NA
            results_KO[j,i] <- NA
            num_changed[j,i] <- 0        
            next
        }
        A2 <- p2[dim(p2)[1],]
        IRR <- not_in_attractors(A0,A2)
        ones = ones + IRR
        if(S0[[i]]==1){
            results_KO[j,i] <- IRR
            results_OE[j,i] <- NA
            rec[j,i] <- 1
        }
        else if(S0[[i]]==0){
            results_OE[j,i] <- IRR
            results_KO[j,i] <- NA
            rec[j,i] <- 0
        }
        if(IRR>0){
            num_changed[j,i] <- changed(A0,A2)
        }
        else{
            num_changed[j,i] <- 0
        }
        
    }
    
    e=Sys.time()
    print(e-s)

}

colnames(results_OE) <- names(p1)
colnames(results_KO) <- names(p1)
colnames(num_changed) <- names(p1)
              
results_OE[epochs+1,] = colMeans(results_OE[1:epochs,], na.rm=T)
results_OE[epochs+2,] = 1- (colSums(rec, na.rm=T)/(epochs-skipped))
results_OE <- results_OE[,order(results_OE[epochs+1,],decreasing=TRUE)]
write.csv(results_OE,fp_result_OE)

results_KO[epochs+1,] = colMeans(results_KO[1:epochs,], na.rm=T)
results_KO[epochs+2,] = colSums(rec, na.rm=T)/(epochs-skipped)
results_KO <- results_KO[,order(results_KO[epochs+1,],decreasing=TRUE)]
write.csv(results_KO,fp_result_KO)



num_changed[epochs+1,] = colSums(num_changed[1:epochs,])/(epochs-skipped)
num_changed <- num_changed[,order(num_changed[epochs+1,],decreasing=TRUE)]
write.csv(num_changed,fp_changed)


