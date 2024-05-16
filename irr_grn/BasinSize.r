library(BoolNet)
library(dplyr)
library(prodlim)


fp = commandArgs()[6]
fp_rs2 = paste('./netfiles/', fp,'.net',sep='')
att.list <- list()
fp_basin = paste('./basins/basinFreqs-',fp,".tsv",sep='')
net <- loadNetwork(fp_rs2)
num_nodes = 87
epochs = 50000
for (j in 1:50000){
    gotoNext <- FALSE
    IS <- sample(c(0,1), replace=TRUE, size=num_nodes)
    p0 <- try(getPathToAttractor(net,IS))
    while(inherits(p0, "try-error")){
        IS <- sample(c(0,1), replace=TRUE, size=num_nodes)
        p0 <- try(getPathToAttractor(net,IS))
    }
    A0 <- p0[attr(p0,'attractor')[1]:dim(p0)[1],]
    ## strategy: convert to integer
    att.no <- paste(as.character(A0[1,]),collapse='')
    for(nm in names(att.list)){
    	#convert the nm to an integer or list thereof
    	for(elt in unlist(strsplit(nm, ', '))){
    		  if(elt==att.no){ 
                  att.list[[nm]] <- att.list[[nm]]+1
                  gotoNext <- TRUE
                  break
              }
    	}
    	if(gotoNext){ break }
    }
    if(gotoNext){ next }
    att.no.vec <- c()
    for(ii in 1:dim(A0)[1]){ 
        att.no.vec <- c(att.no.vec,paste(as.character(A0[ii,]),collapse=''))
    }
    att.nm <- paste(att.no.vec, collapse=', ')
    att.list[[att.nm]] <- 1
}
op.cat <- c()
for (name in names(att.list)) {
    value <- att.list[[name]]
    op.cat <- c(op.cat,paste(name,value,sep='\t'))
}
writeLines(op.cat,fp_basin)
