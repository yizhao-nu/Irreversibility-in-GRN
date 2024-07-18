#!/usr/bin/env bash

## Statement to get the max number of cpus on a machine
cpus=$( ls -d /sys/devices/system/cpu/cpu[[:digit:]]* | wc -w ) ## can CHANGE to an integer to set the max number of processes
#cpus=18
## Function to make the number of CPUs match the number of processes
function pwait() {
	while [ $(ps -u | grep -v "grep" | grep -c "try_KO_pre_chunked.r") -ge $1 ]; do
        wait -n ## change to ""sleep 1"" if using bash version <4.3
    done
}

fps=('twoparam_0.00_0.40_asc_02_2' 'twoparam_0.00_0.40_asc_10_10' 'twoparam_0.20_0.80_asc_09_9' 'twoparam_0.20_0.80_asc_17_17' 'twoparam_0.20_1.00_asc_08_8' 'twoparam_0.40_0.60_asc_00_0' 'twoparam_0.40_0.60_asc_08_8' 'twoparam_0.40_0.60_asc_14_14' 'twoparam_0.40_0.60_asc_19_19' 'twoparam_0.40_1.00_asc_00_0' 'twoparam_0.40_1.00_asc_02_2' 'twoparam_0.40_1.00_asc_03_3' 'twoparam_0.40_1.00_asc_05_5' 'twoparam_0.40_1.00_asc_08_8' 'twoparam_0.40_1.00_asc_09_9' 'twoparam_0.40_1.00_asc_10_10' 'twoparam_0.40_1.00_asc_11_11' 'twoparam_0.40_1.00_asc_17_17' 'twoparam_0.80_1.00_asc_07_7' 'twoparam_0.80_1.00_asc_01_1' 'twoparam_0.60_1.00_asc_16_16' 'twoparam_0.40_1.00_asc_18_18')

for fp in ${fps[@]}; do
    echo "${fp}"
    for ((ii=1; ii<=${cpus}; ii++)); do
	echo "chunk ${ii} of ${cpus}"
    	nohup Rscript try_KO_pre_chunked.r "${fp}" ${ii} ${cpus} > ./logging/${fp}_chunk_${ii}_of_${cpus}.txt 2>&1 & 
        pwait $cpus
    done
done
