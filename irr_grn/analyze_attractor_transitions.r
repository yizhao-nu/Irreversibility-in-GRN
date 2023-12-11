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
attr.strings <- apply(attrs.df,1,function(x){ paste0(x,collapse="")})


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
changed.identity <- function(ai,af,getState){
    ## now, getState=T takes over the nearest.state functionality
    # getState=F gets the irreversible response genes
    if(length(dim(ai))>1){
        ai.row <- ai[1,]
    }
    else{
        ai.row <- ai
    }
    CNS <- names(ai.row)
    if(length(dim(af))>1){
        ## if the final attractor is periodic, need to find the closest state
        min.hamm <- ncol(af)
        min.ind <- 0
        for (ii in 1:nrow(af)){
            af.row <- af[ii,]
            hamm <- sum(abs(ai.row-af.row))
            if (hamm<min.hamm){
                min.hamm <- hamm
                min.ind <- ii
                if(min.hamm<2){break}
            }
        }
        af.row <- af[min.ind,] ## determine the changes from here
    }
    else{
        af.row <- af
    }
    if(getState){
        return(af.row)
    }
    else{
        diffs <- abs(ai.row-af.row)
        cns <- CNS[which(diffs!=0,arr.ind = T)]
        return(cns[!duplicated(cns)])
    }
}
file.headers <- c('init_attr_index', 'pert_gene_name', 'attr_size_equal', 'fixed_set_equal', 'is_fixed_changed','num_fixed_changed','init_num_fixed','fin_num_fixed', 'fin_attr_index')

for(pt in c('OE','KO')){
    ## create the output file string
    changed.vec.file <- paste('./results/')
    ## read the lines in the result file, with a counter or otherwise
    fp_result = paste('./results/result-',pt,'-',fp,'-pre.csv',sep='')
    results.df <- read.csv(fp_result,stringsAsFactors = F,check.names = F,row.names=1)
    results.df <- results.df[1:(nrow(results.df)-2),]
    trans_result = paste('./results/result-attr-trans-',pt,'-',fp,'.csv',sep='')
    changed.vec.str <- character(length=sum(results.df,na.rm=TRUE)+1)
    changed.vec.str[1] <- paste(file.headers,collapse=',')
    gene.names <- colnames(results.df)
    line.no <-2
    ## iterate over the rows of results.df
    for (k in 1:nrow(results.df)){
        #print(k)
        res.row <- results.df[k,]
        S0 <- attrs.df[k,]
        S0.attr <- getPathToAttractor(net,S0,includeAttractorStates = 'all')
        S0.attr <- sapply(S0.attr, as.numeric)
        if(length(dim(S0.attr))>1){
            init.attr.size <- nrow(S0.attr)
        }
        else{
            init.attr.size <- 1
        }
        
        if (init.attr.size<2){
            fixed.genes.0 <- names(S0.attr)
            var.genes.0 <- c()
        }
        else{
            state.sums <- colSums(S0.attr)
            lvec <- sapply(state.sums, function(x){(x==0)|(x==nrow(S0.attr))})
            fixed.genes.0 <- names(which(lvec)) ## condition for being fixed
            var.genes.0 <- names(which(!lvec)) ## condition for being variable
        }
        for (colnm in colnames(results.df)){
            l <- grep(paste('^',colnm,'$',sep=''),colnames(attrs.df))
            if (is.na(res.row[colnm])){next}
            if (res.row[colnm]==1){
                S1 <- alterState(S0,l)
                new.i <- S1[[l]]
                N1 <- fixGenes(net,l,new.i)
                p1 <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'first'))
                if(inherits(p1, "try-error")){
                    #error handling code, maybe just skip this iteration using
                    #probably want to change this to raising an error
                    next
                }
                A1 <- lapply(p1[dim(p1)[1],],as.numeric)
                S1.attr <- getPathToAttractor(N1,A1,includeAttractorStates = 'all')
                S1.attr <- sapply(S1.attr, as.numeric)
                A1 <- changed.identity(S0.attr,S1.attr,T)
                N2 <- fixGenes(N1,l,-1)
                A1[[l]] <- 1 - new.i
                p2 <- getPathToAttractor(N2,A1,includeAttractorStates = 'first')
                A2 <- p2[dim(p2)[1],]
                S2.attr <- getPathToAttractor(N2,unlist(A2),includeAttractorStates = "all")
                S2.attr <- sapply(S2.attr, as.numeric)
                if(length(dim(S2.attr))>1){
                    fin.attr.size <- nrow(S2.attr)
                }
                else{
                    fin.attr.size <- 1
                }                
                if (fin.attr.size<2){
                    fixed.genes.2 <- names(S2.attr)
                    var.genes.2 <- c()
                }
                else{
                    state.sums <- colSums(S2.attr)
                    lvec <- sapply(state.sums, function(x){(x==0)|(x==nrow(S2.attr))})
                    fixed.genes.2 <- names(which(lvec)) ## condition for being fixed
                    var.genes.2 <- names(which(!lvec)) ## condition for being variable                
                }
                ## need to find ANY difference in the hamming distance between the two genes
                changed <- changed.identity(S0.attr,S2.attr,F)
                ## need to compare the genes that changed with the fixed & variable sets of genes
                ## 1. check that fixed== fixed and 2. variable == variable
                is.fixed.equal <- setequal(fixed.genes.2,fixed.genes.0) ## if is.fixed.equal, then var is equal
                ## 2. check that attractor sizes are the same
                is.size.equal <- (init.attr.size==fin.attr.size)
                ## 3. check whether the irreversible difference is in the fixed genes only, the variable genes only, or both
                fixed.changed <- intersect(changed,fixed.genes.2)
                is.fixed.changed <- setequal(fixed.changed,changed)
                ## how to figure out fin_attr_index?
                ## which row of attrs.df matches S2? match(S2,attrs.df, nomatch=0)
                fin.attr.index <- 0
                if(length(dim(S2.attr))>1){
                    for (m in 1:nrow(S2.attr)){
                        row.str <- paste0(S2.attr[m,],collapse="")
                        if (row.str %in% attr.strings){
                            fin.attr.index <- match(row.str, attr.strings,nomatch=0)
                            break
                        }
                    }
                }
                else{
                    row.str <- paste0(S2.attr,collapse="")
                    if (row.str %in% attr.strings){
                        fin.attr.index <- match(row.str, attr.strings,nomatch=0)
                    }                    
                }
                if (fin.attr.index<1){
                    print("no matching attractor found!")
                } 
                ## 4. output this information to a file.
                ## need to output to a line of the file
                ## c('init_attr_index', 'pert_gene_name', 'attr_size_equal', 'fixed_set_equal', 'is_fixed_changed','num_fixed_changed', 'init_num_fixed', 'fin_num_fixed', 'fin_attr_index')
                line.data <- c(k,colnm,is.size.equal, is.fixed.equal, is.fixed.changed, length(fixed.changed) ,length(fixed.genes.0),length(fixed.genes.2),fin.attr.index)
                changed.vec.str[line.no] <- paste(as.character(line.data),collapse=',')
                line.no <- line.no +1
            }
        }
    }
    writeLines(changed.vec.str, trans_result)   
}
print('Done!')
## 

