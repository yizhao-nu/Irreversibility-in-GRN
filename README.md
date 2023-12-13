# Irreversibility-in-GRN
Code associated with the manuscript "Irreversibility in Bacterial Regulatory Networks"

## Installation instructions

### Step 1: Create a virtual environment. 
The packages (other than bns and pyboolnet) may be obtained from the conda package management software. 
We recommend using the [miniforge distribution](https://github.com/conda-forge/miniforge) of conda, which offers a substantially faster dependency solver that can be invoked by replacing `conda` with `mamba` in the above command. 
See details at the link for installation.

It is possible to create a virtual environment with the packages using the command:

`mamba create env -n irrev-in-gn-nets -c conda-forge python=3.10 gh git jupyter matplotlib networkx numpy openpyxl pandas patsy scipy scikit-learn sympy r-essentials r-base r-dplyr r-BoolNet`


#### Initially installed packages

The following packages are installed upon creating the environment:

* gh: GitHub command line interface
* git: git version control sofrware
* jupyter: python library for viewing python notebooks, used for running commands interactively
* matplotlib: python plotting library, used for generating figures
* networkx: python network algorithms, analysis, and layout library
* numpy: numerical python library
* openpyxl: python library for opening excel files
* pandas: python data-science library, used for creating dataframes
* patsy: python statistical modeling library
* scipy: python scientific computing library
* scikit-learn: python machine-learning library
* sympy: python symbolic mathematics library
* r-dplyr: R data manipulation grammar
* r-BoolNet: R Boolean network library

Note that the environment is based on Python v. 3.10.

### Step 2: Install additional dependencies
After creating the virtual environment, activate the environment by typing

`mamba activate irrev-in-gn-nets`

Then, install the following packages:
* pyboolnet (Enter `pip install git+https://github.com/hklarner/pyboolnet` at the command line)
* bns (download the source code from https://people.kth.se/~dubrova/BNS/bns_v1.3.zip and follow the instructions in the README file)

### Step 3: Clone the repository
After compiling `bns`, clone the repository (e.g., using the command `gh repo clone https://github.com/yizhao-nu/Irreversiblility-in-GRN`). 
Next, copy the `bns` executable (`bns.exe` on Windows) into the `irr_grn` directory.
If you cloned the repository into the same directory that you downloaded `bns_v1.3.zip` into, then
the command

`cp bns_v1.3/src/bns irr_grn/bns`

or the Windows equivalent will copy the executable of the `bns` program into the repository.


## Files in the repository
### RegulonDB files
The most recent version of RegulonDB can be downloaded from https://regulondb.ccg.unam.mx/menu/download/full_version/index.jsp. We include the file `irr_grn/input_files/generegulation_tmp.txt` downloaded on Jun 17, 2019.

### Walkthrough of the analysis pipeline
The steps of the analysis pipeline are described by the `README.md` in the `irr_grn` directory.

### Scripts and notebooks

#### Scripts for processing the input data, generating rules, finding attractors, and characterizing transitions.
The file `irr_grn/read_reduce_grn.py` reads in the RegulonDB network and reduces it to its core.

The file `irr_grn/generate_nets.py` contains the algorithm for generating the rules for different values of the parameter $r$. This script requires the pyboolnet package to perform the logic reduction of the rules.

The file `irr_grn/bns.sh` applies the attractor finding algorithm of Dubrova et al. (doi:10.1109/TCBB.2010.20) and requires the `bns` executable that can be obtained and compiled as described in Step 2 above.

The file `irr_grn/attcsv.sh` processes the found attractors as an input to the irreversibility detection algorithm.

The file `irr_grn/simulation.sh` performs the irreversibility detection algorithm.
This script invokes the R script `try_KO_pre.r`. 

The file `irr_grn/irr_resp_gns.sh` calculates the irreversible response genes to the knockout and overexpression of _crp_ according to the Boolean model.
The script invokes the R script `irr_grn/analyze_crp_irr_resp_gns.r` 

The file `irr_grn/attr_trans.sh` performs the analysis of the attractor transitions.
The script invokes the R script `irr_grn/analyze_attractor_transitions.r`. 

#### Notebooks for generating the figures of the paper.

The notebook `irr_grn/irr_prob.ipynb`:

1. Analyzes the relationship of the parameters $r$ and $s$ to the rule bias and canalization depth in Fig. 3,
2. Generates the graph featured in Fig. 4 of the paper, and
3. Generates Figs. 5, 6, and S1.

The notebook `irr_grn/case_study.ipynb` contains details regarding the RNA-seq data preprocessing, in addition to the code for generating Fig. 7B and associated statistical analyses.

The output of this script is used in `irr_grn/attractor_diff.ipynb` to calculate:

1. The fraction of attractors that have each period length,
2. The fraction of transitions that occur between two fixed points, a fixed point and a partial fixed point, two partial fixed points with the same set of time-dependent nodes, and two partial fixed points with different sets of time-dependent nodes, and
3. The fraction of transitions involving at least one partial fixed point for which both the initial and final attractors are guaranteed to be preserved.

These are used to compute the percentages referenced in the Supplementary Information.
