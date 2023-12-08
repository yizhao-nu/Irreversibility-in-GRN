# Analysis pipeline
Analysis of the network irreversibility proceeds according to the following procedure: 

## Convert RegulonDB network to GraphML file
Run the command `python read_reduce_grn.py`. This will create the file `networks/rs2.gml`.

## Generate networks
Run the command `./generate_nets.sh`.
This will generate network files in the `netfiles/` directory.
There should be 20 for each value of $r$ and $s$ considered in the manuscript (except those that lead to unique rules). 


