#!/usr/bin/env bash

## Statement to get the max number of cpus on a machine
cpus=$( ls -d /sys/devices/system/cpu/cpu[[:digit:]]* | wc -w ) ## can CHANGE to an integer to set the max number of processes
## Function to make the number of CPUs match the number of processes
function pwait() {
	while [ $(ps -u | grep -v "grep" | grep -c "find_rev_genes.r") -ge $1 ]; do
        wait -n ## change to ""sleep 1"" if using bash version <4.3
    done
}


gns=('crp')
ps=(0.20 0.40 0.60 0.80)
ord=('asc' 'desc')
for gn in ${gns[@]}; do
echo $gn
if [ ! -d "./logging/${gn}" ]; then
    mkdir "./logging/${gn}"
fi
if [ ! -d "./results/${gn}" ]; then
    mkdir "./results/${gn}"
fi

for order in ${ord[@]}; do
    for p in ${ps[@]}; do
        q1=$(bc -l <<<"1-${p}")
        printf -v q11 "%.02f" ${q1}
        printf -v pp '%.02f' ${p}
        for i in {0..19}; do
            printf -v ii '%02d' ${i}
            if [ ! -f "./logging/${gn}/a1_twoparam_${pp}_${q11}_${order}_${ii}_${i}_${gn}.txt" ]; then 
                echo "${pp}_${q11}_${order}_${ii}_${i}" "${gn}"
                nohup Rscript find_rev_genes.r "twoparam_${pp}_${q11}_${order}_${ii}_${i}" "${gn}" > ./logging/${gn}/a1_twoparam_${pp}_${q11}_${order}_${ii}_${i}_${gn}.txt 2>&1 & 
                pwait $cpus
            fi
            if [ ! -f "./logging/${gn}/a1_twoparam_${pp}_1.00_${order}_${ii}_${i}_${gn}.txt" ]; then 
                echo "${pp}_1.00_${order}_${ii}_${i}" "${gn}"
                nohup Rscript find_rev_genes.r "twoparam_${pp}_1.00_${order}_${ii}_${i}" "${gn}" > ./logging/${gn}/a1_twoparam_${pp}_1.00_${order}_${ii}_${i}_${gn}.txt 2>&1 & 
                pwait $cpus
            fi
            if [ ! -f "./logging/${gn}/a1_twoparam_0.00_${pp}_${order}_${ii}_${i}_${gn}.txt" ]; then 
                echo "0.00_${pp}_${order}_${ii}_${i}" "${gn}"
                nohup Rscript find_rev_genes.r "twoparam_0.00_${pp}_${order}_${ii}_${i}" "${gn}" > ./logging/${gn}/a1_twoparam_0.00_${pp}_${order}_${ii}_${i}_${gn}.txt 2>&1 & 
                pwait $cpus
            fi
        done
    done
    if [ ! -f "./logging/${gn}/a1_twoparam_1.00_0.00_${order}_00_0_${gn}.txt" ]; then 
        echo "twoparam_1.00_0.00_${order}_00_0" "${gn}"
        nohup Rscript find_rev_genes.r "twoparam_1.00_0.00_${order}_00_0" "${gn}" > ./logging/${gn}/a1_twoparam_1.00_0.00_${order}_00_0_${gn}.txt 2>&1 & 
        pwait $cpus
    fi
    if [ ! -f "./logging/${gn}/a1_twoparam_0.00_1.00_${order}_00_0_${gn}.txt" ]; then 
        echo "twoparam_0.00_1.00_${order}_00_0" "${gn}"
        nohup Rscript find_rev_genes.r "twoparam_0.00_1.00_${order}_00_0" "${gn}" >  ./logging/${gn}/a1_twoparam_0.00_1.00_${order}_00_0_${gn}.txt 2>&1 & 
        pwait $cpus
    fi
done
done
wait