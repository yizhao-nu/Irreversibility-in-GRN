# Analysis pipeline
Analysis of the network irreversibility proceeds according to the following procedure: 

## Convert RegulonDB network to GraphML file
Run the command `python read_reduce_grn.py`. This will create the file `networks/rs2.gml`.

## Generate networks
Run the command `./generate_nets.sh`.
This will generate network files in the `netfiles/` directory.
There should be 20 for each value of $r$ and $s$ considered in the manuscript (except those that lead to unique rules). 

## Find attractors
Run the command `./bns.sh`.
This will generate the attractors, which are stored in the `attfiles/` directory.

Run the command `./attcsv.sh`.
This will generate the files that contain the first states of the attractors, which will be used to detect irreversibility.

## Run the irreversibility detection algorithm
Run the command `./simulation.sh`

This command runs the script `try_KO_pre.r`, which executes the irreversibility detection algorithm. It is designed to use all available processes on the computer. 
Full recalculation of the results takes approximately 3,000 hours on a single processor.
Therefore, it is recommended to take advantage of a computing cluster. 
The maximum number of processes can be controlled by altering line 4 (starting with `cpus`) to be equal to the desired maximum number of processes.
Use of the `wait -n` command on line 8 (inside the function pwait) requires bash version $\geq 3.4$. 
If using an older version of bash, change the line to `sleep 1`.
Finally, the script's default behavior is to skip any files that have been previously completed.
If recalculation of existing files is needed, they will need to first be removed from the `results/` directory.

## Analyze the attractor transitions
Run the command `./attr_trans.sh`

This command runs the script `analyze_attractor_transitions.r`, which characterizes the starting and ending attractors for each transition.
The options described for the script `simulation.sh` apply (see preceding section). 



