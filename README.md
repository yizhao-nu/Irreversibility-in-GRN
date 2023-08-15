# Irreversiblility-in-GRN
Code associated with the manuscript "Irreversibility in gene regulatory networks"

## Files in the repository
### RegulonDB files
The most recent version of RegulonDB can be downloaded from https://regulondb.ccg.unam.mx/menu/download/full_version/index.jsp. We include the file "irr_grn/input_files/generegulation_tmp.txt" downloaded on Jun 17, 2019.

### Walkthrough of the analysis pipeline
The steps of the analysis pipeline are described by the `README.md` in the `irr_grn` directory.

### Scripts and notebooks
The file `irr_grn/read_reduce_grn.py` reads in the RegulonDB network and reduces it to its core.

The file `generate_nets.py` contains the algorithm for generating the rules for different values of the parameter $r$. This script requires the pyboolnet package to perform the logic reduction of the rules. This package may be obtained from the  github repo https://github.com/hklarner/pyboolnet by following the instructions on the README page.

The file `bns.sh` applies the attractor finding algorithm of Dubrova et al. (doi:10.1109/TCBB.2010.20) and requires a compiled version of the code available at https://people.kth.se/~dubrova/BNS/bns_v1.3.zip. Compilation instructions are available in the README file of the zipped package. We provide compiled versions in this repository (`bns.exe` for Windows systems and `bns` for Mac/Linux systems).

The file `attcsv.sh` processes the found attractors as an input to the irreversibility detection algorithm.

The file `try_KO_pre.r` performs the irreversibility detection algorithm.

The notebook `irr_prob.ipynb` generates the graph featured in Fig. 3 of the paper, Fig. 4, and Fig. 5. It also analyzes the relationship of the parameter $r$ to the number of monomials, canalization, and bias of the rules in Fig. S2. 

The file `variability.py` performs the analysis of the variability of the irreversibility probability as featured in Fig. S3. 

The notebook `case_study.ipynb` contains details regarding the RNA-seq data preprocessing, in addition to the code for generating Fig. 6 and Figs. S4 and S5.

## System requirements

This repository requires the following python packages:

jupyter
networkx
matplotlib
numpy
openpyxl
pandas
patsy
scipy
sympy
scikit-learn
pyboolnet (see instructions at https://github.com/hklarner/pyboolnet)
bns (see instructions above)

This repository also requires the following R packages:
dplyr
BoolNet

The packages (other than bns and pyboolnet) may be obtained from the conda package management software. It is possible to create a virtual environment with the packages using the command:
`mamba create env -n irrev-in-gn-nets -c conda-forge numpy scipy pandas networkx matplotlib sympy openpyxl jupyter patsy scikit-learn`
