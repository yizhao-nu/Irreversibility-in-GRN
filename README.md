# Irreversiblility-in-GRN
Code associated with the manuscript "Irreversibility in Bacterial Regulatory Networks"

## System requirements

The packages (other than bns and pyboolnet) may be obtained from the conda package management software. It is possible to create a virtual environment with the packages using the command:
`conda create env -n irrev-in-gn-nets -c conda-forge gh git jupyter matplotlib networkx numpy openpyxl pandas patsy scipy scikit-learn sympy r-dplyr r-BoolNet`

We recommend using the [miniforge distribution](https://github.com/conda-forge/miniforge) of conda, which offers a substantially faster dependency solver that can be invoked by replacing `conda` with `mamba` in the above command. See details at the link for installation.

This repository requires the following python packages:

### Initially installed packages

The following packages are installed upon creating the environment:

gh: GitHub command line interface

git: git version control sofrware

jupyter: python library for viewing python notebooks, used for running commands interactively

matplotlib: python plotting library, used for generating figures

networkx: python network algorithms, analysis, and layout library

numpy: numerical python library

openpyxl: python library for opening excel files

pandas: python data-science library, used for creating dataframes

patsy: python statistical modeling library

scipy: python scientific computing library

scikit-learn: python machine-learning library

sympy: python symbolic mathematics library

r-dplyr: R data manipulation grammar

r-BoolNet: R Boolean network library

### Packages to be installed separately

pyboolnet (see instructions at https://github.com/hklarner/pyboolnet)

bns (see instructions below)

## Files in the repository
### RegulonDB files
The most recent version of RegulonDB can be downloaded from https://regulondb.ccg.unam.mx/menu/download/full_version/index.jsp. We include the file `irr_grn/input_files/generegulation_tmp.txt` downloaded on Jun 17, 2019.

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

