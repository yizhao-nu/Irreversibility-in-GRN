library(BoolNet)
library(dplyr)

fp = commandArgs()[6]
gn = commandArgs()[7]
print(fp)
fp_rs2 <- paste('./netfiles/', fp,'.net',sep='')
fp_unique <- paste('./attfiles/','1st_',fp,".csv",sep='')
attrs.df <- read.csv(fp_unique,header=FALSE)
net <- loadNetwork(fp_rs2)
colnames(attrs.df) <- net$genes
print(dim(attrs.df))

          

fp_revgn_KO = paste('./results/',gn,'/rev-changed-KO-',fp,'-pre.csv',sep='')
fp_revgn_OE = paste('./results/',gn,'/rev-changed-OE-',fp,'-pre.csv',sep='')
fp_irrevgn_KO = paste('./results/',gn,'/irrev-changed-KO-',fp,'-pre.csv',sep='')
fp_irrevgn_OE = paste('./results/',gn,'/irrev-changed-OE-',fp,'-pre.csv',sep='')
fp_a1KO_result = paste('./results/',gn,'/a1-irrgn-KO-',fp,'-',gn,'.csv',sep='')
fp_a1OE_result = paste('./results/',gn,'/a1-irrgn-OE-',fp,'-',gn,'.csv',sep='')
#fp_changed = paste('./results/',gn,'/changed-pre-',fp,'.csv',sep='')


alterState <- function(S,i){
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

num_nodes <- 87

epochs = dim(attrs.df)[1]
print(epochs)
revgn_KO <- matrix(NA, epochs, num_nodes)
revgn_OE <- matrix(NA, epochs, num_nodes)
irrevgn_KO <- matrix(NA, epochs, num_nodes)
irrevgn_OE <- matrix(NA, epochs, num_nodes)
a1KO_result <- matrix(NA, epochs, num_nodes)
a1OE_result <- matrix(NA, epochs, num_nodes)


ones <- 0  ##  counter for the attractors
gn.ind <- grep(paste("^", gn, "$", sep=""), colnames(attrs.df))

####### use found attractors #######
for (j in 1:epochs){ 
    start <- apply(attrs.df[j,], 1, function(r){ paste(r)}) ## converts to character
    IS <- as.numeric(unlist(start))
    p0 <- try(getPathToAttractor(net,IS,includeAttractorStates = 'first'))
    if (inherits(p0,'try-error')){ next }
    A0 <- p0[attr(p0,'attractor'),]
    S0 <- A0[1,]
    
    S1 <- alterState(S0,gn.ind)
    new_i = S1[gn.ind]
    N1 <- fixGenes(net,gn.ind,new_i)
    p1 <- try(getPathToAttractor(N1,S1,includeAttractorStates = 'first'))
    if(inherits(p1, "try-error")){
        revgn_KO[j,] <- NA
        irrevgn_KO[j,] <- NA
        revgn_OE[j,] <- NA
        irrevgn_OE[j,] <- NA
        a1KO_result[j,] <- NA
        a1OE_result[j,] <- NA
        next
    }
    A1 <- lapply(p1[dim(p1)[1],],as.numeric)
    if(S0[[gn.ind]]==1){
        a1KO_result[j,] <- unlist(A1)
        a1OE_result[j,] <- NA
        }
    else{
        a1KO_result[j,] <- NA
        a1OE_result[j,] <- unlist(A1)
    }
    intermed <- changed.identity(S0,A1,colnames(attrs.df))
    N2 <- fixGenes(N1,gn.ind,-1)
    A1[gn.ind] = 1 - new_i
    p2 <- try(getPathToAttractor(N2,A1,includeAttractorStates = 'first'))
    if(inherits(p2, "try-error")){
        revgn_KO[j,] <- NA
        irrevgn_KO[j,] <- NA
        revgn_OE[j,] <- NA
        irrevgn_OE[j,] <- NA
        next
    }
    A2 <- p2[dim(p2)[1],]
    final <- changed.identity(as.data.frame(A1),A2,colnames(attrs.df))
    rev.gnset <- intersect(intermed,final)
    irrev.gnset <- setdiff(union(intermed,final), rev.gnset)
    if(S0[[gn.ind]]==1){
        for (gg in 1:length(rev.gnset)){
            rgn.ind <- grep(paste("^", rev.gnset[[gg]], "$", sep=""),colnames(attrs.df))
            revgn_KO[j,rgn.ind] <- 1
        }
        revgn_OE[j,] <- NA
        for (gg in 1:length(irrev.gnset)){
            irrgn.ind <- grep(paste("^", irrev.gnset[[gg]], "$", sep=""),colnames(attrs.df))
            irrevgn_KO[j,irrgn.ind] <- 1
        }
        irrevgn_OE[j,] <- NA
    }
    else if(S0[[gn.ind]]==0){
        for (gg in 1:length(rev.gnset)){
            rgn.ind <- grep(paste("^", rev.gnset[[gg]], "$", sep=""),colnames(attrs.df))
            revgn_OE[j,rgn.ind] <- 1
        }
        revgn_KO[j,] <- NA
        for (gg in 1:length(irrev.gnset)){
            irrgn.ind <- grep(paste("^", irrev.gnset[[gg]], "$", sep=""),colnames(attrs.df))
            irrevgn_OE[j,irrgn.ind] <- 1
        }
        irrevgn_KO[j,] <- NA
    }

}

colnames(revgn_OE) <- colnames(attrs.df)
colnames(revgn_KO) <- colnames(attrs.df)
colnames(irrevgn_OE) <- colnames(attrs.df)
colnames(irrevgn_KO) <- colnames(attrs.df)
colnames(a1KO_result) <- colnames(attrs.df)
colnames(a1OE_result) <- colnames(attrs.df)
        
write.csv(revgn_OE,fp_revgn_OE)
write.csv(revgn_KO,fp_revgn_KO)
write.csv(irrevgn_OE,fp_irrevgn_OE)
write.csv(irrevgn_KO,fp_irrevgn_KO)
write.csv(a1KO_result,fp_a1KO_result)
write.csv(a1OE_result,fp_a1OE_result)
