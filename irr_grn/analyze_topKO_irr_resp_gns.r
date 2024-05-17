library(BoolNet)
library(dplyr)

fp = commandArgs()[6] ## name of the file
gn = commandArgs()[7]
## result input files
print(fp)
fp_rs2 <- paste('./netfiles/', fp,'.net',sep='') ## network rules
fp_unique <- paste('./attfiles/','1st_',fp,".csv",sep='') ## attractors
attrs.df <- read.csv(fp_unique,header=F)



## result output files

net <- loadNetwork(fp_rs2)
colnames(attrs.df) <- net$genes
alterState <- function(S,i){
    S[i] <- 1- S[i]
    return(S)
}

not_in_attractors <- function(atts,a){
    num_atts = dim(atts)[1]
    atts[num_atts+1,] = lapply(a,as.numeric)
    atts2 <- distinct(atts)
    num_atts2 <- dim(atts2)[1]   
    if (num_atts == num_atts2){c <- 0}
    else {c <- 1}
    return(c)
}

## write a function to identify the identities of the changed genes.
changed.identity <- function(atts,a,COLNAMES){
    changed.set = c()
    for (i in 1:dim(atts)[1]){
        ## for each attractor determine which genes are changed
        cns <- COLNAMES[which(atts[i,]!=a)]
        distinct.diffs.set <- cns[!duplicated(cns)]
        changed.set <- union(changed.set,distinct.diffs.set)        
    }
    return(changed.set)
}

closest.approach <- function(init.attr,fin.attr){
    max.hamm.dist <- dim(init.attr)[2] ## note for very large attractors this could fail
    jj.min <- 1
    ii.min <- 1
    for(ii in seq_len(nrow(init.attr))){
        for(jj in seq_len(nrow(fin.attr))){
            x.hamm.dist <- sum(sapply(fin.attr[jj,],as.numeric) != sapply(init.attr[ii,],as.numeric))
            if(x.hamm.dist<max.hamm.dist){
                jj.min <- jj
                ii.min <- ii
            }
        }
    }
    return(c(ii.min,jj.min))
}

num_nodes <- 87
pt <- 'KO'

## read the lines in the result file, with a counter or otherwise
fp_result = paste('./results/result-',pt,'-',fp,'-pre.csv',sep='')
results.df <- read.csv(fp_result,stringsAsFactors = F,check.names = F,row.names=1)
results.df <- results.df[1:(nrow(results.df)-2),]
TF <- results.df[,gn]==1
TF[is.na(TF)] <- F
if (sum(TF)==0){
    print(paste("No irreverisible cases:",pt,fp,sep='\t'))
    next
}
## create the output file string
gn_result = paste('./results/',gn,'/result-irrgn-',pt,'-',fp,'-',gn,'.csv',sep='') 

## restrict to the lines that are found to be irreversible
gn.irr.df <- results.df[TF,]
#start = apply(attrs.df, 2, function(r){paste(r)}) ## converts to character
changed.vec.str <- character(length=dim(gn.irr.df)[1])
## for each line we need to get the rownames
indices <- row.names(gn.irr.df)
gn.ind <- grep(paste("^", gn, "$", sep=""), colnames(attrs.df))
print(nrow(gn.irr.df))

for(k in seq_len(nrow(gn.irr.df))){
    S0 <- attrs.df[indices[k],]
    S0.all <- try(getPathToAttractor(net,S0,includeAttractorStates = 'all'))
    ## need to alter crp state
    S0.attr <- S0.all[attr(S0.all,'attractor'),]
    S1 <- alterState(S0,gn.ind)
    new_i <- S1[[gn.ind]]
    N1 <- fixGenes(net,gn.ind,new_i)
    p1.all <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'all'))
    if(inherits(p1.all, "try-error")){
        #error handling code, maybe just skip this iteration using
        #probably want to change this to raising an error
        changed.vec.str[k] <- paste(indices[k],'NA',sep='\t')
        next
    }
    p1.attr <- p1.all[attr(p1.all,'attractor'),]
    ind.pair <- closest.approach(p1.attr,S0.attr)
    ii.min <- ind.pair[1]
    jj.min <- ind.pair[2]
    A1 <- lapply(p1.attr[jj.min,],as.numeric)
    N2 <- fixGenes(N1,gn.ind,-1)
    A1[[gn.ind]] <- 1 - new_i
    p2.all <- try(getPathToAttractor(N2,A1,includeAttractorStates = 'all'))
    if(inherits(p2.all, "try-error")){
        #error handling code, maybe just skip this iteration using
        #probably want to change this to raising an error
        changed.vec.str[k] <- paste(indices[k],'NA',sep='\t')
        next
    }
    p2.attr <- p2.all[attr(p2.all,'attractor'),]
    ind.pair.2 <- closest.approach(p2.attr,S0.attr)
    ii.min.2 <- ind.pair[1]
    jj.min.2 <- ind.pair[2]
    A2 <- p2.attr[jj.min.2,]
    changed <- changed.identity(S0,A2,colnames(attrs.df))
    #changed <- setdiff(changed,c(gn))
    if(length(changed)>0){
        csv.changed.gn <- paste(as.character(changed), collapse=", ")
        changed.vec.str[k] <- paste(indices[k],csv.changed.gn,sep='\t')
    }
    else{
        changed.vec.str[k] <- paste(indices[k],'NA',sep='\t')
    }
}

writeLines(changed.vec.str, gn_result)

print('Done!')
## 

