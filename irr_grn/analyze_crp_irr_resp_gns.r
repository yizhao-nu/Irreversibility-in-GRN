library(BoolNet)
library(dplyr)

fp = commandArgs()[6] ## name of the file
#fp <- 'twoparam_0.00_0.00_desc_00_0'
## this file should be run after the irreversibility detection alg.
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
changed.identity <- function(atts,a){
    changed.set = c()
    for (i in 1:dim(atts)[1]){
        ## for each attractor determine which genes are changed
        diffs <- abs(atts[i,]-lapply(a,as.numeric)) ## these are the set of changed genes
        cns <- colnames(a)[which(diffs!=0,arr.ind = T)]
        distinct.diffs.set <- cns[!duplicated(cns)]
        changed.set <- union(changed.set,distinct.diffs.set)        
    }
    return(changed.set)
}

num_nodes = 87
pts <- c('OE','KO')
for (j in 1:length(pts)){
    pt <- pts[j]
    print(pt)
    ## read the lines in the result file, with a counter or otherwise
    fp_result = paste('./results/result-',pt,'-',fp,'-pre.csv',sep='')
    results.df <- read.csv(fp_result,stringsAsFactors = F,check.names = F,row.names=1)
    results.df <- results.df[1:(nrow(results.df)-2),]
    TF <- results.df$crp==1
    TF[is.na(TF)] <- F
    if (sum(TF)==0){
        print(paste("No irreverisible cases:",pt,fp,sep='\t'))
        next
    }
    ## create the output file string
    crp_result = paste('./results/crp/result-irrgn-',pt,'-',fp,'.csv',sep='') 

    ## restrict to the lines that are found to be irreversible
    crp.irr.df <- results.df[TF,]
    #start = apply(attrs.df, 2, function(r){paste(r)}) ## converts to character
    changed.vec.str <- character(length=dim(crp.irr.df)[1])
    epochs = dim(crp.irr.df)[1]
    ## for each line we need to get the rownames
    indices <- row.names(crp.irr.df)
    crp.ind <- grep("^crp$", colnames(attrs.df))
    print(nrow(crp.irr.df))
    for (k in seq_len(nrow(crp.irr.df))){
        S0 <- attrs.df[indices[k],]
        ## need to alter crp state
        S1 <- alterState(S0,crp.ind)
        new_i <- S1[[crp.ind]]
        N1 <- fixGenes(net,crp.ind,new_i)
        p1 <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'first'))
        if(inherits(p1, "try-error")){
            #error handling code, maybe just skip this iteration using
            #probably want to change this to raising an error
            next
        }
        A1 <- lapply(p1[dim(p1)[1],],as.numeric)
        N2 <- fixGenes(N1,crp.ind,-1)
        A1[[crp.ind]] <- 1 - new_i
        p2 <- getPathToAttractor(N2,A1,includeAttractorStates = 'first')
        A2 <- p2[dim(p2)[1],]
        changed <- changed.identity(S0,A2)
        changed <- setdiff(changed,c('crp'))
        csv.changed.gn <- paste(as.character(changed), collapse=", ")
        changed.vec.str[k] <- paste(indices[k],'\t',csv.changed.gn)
    }
    writeLines(changed.vec.str, crp_result)
    
}
print('Done!')
## 

