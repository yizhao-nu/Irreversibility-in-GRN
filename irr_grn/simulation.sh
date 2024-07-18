#!/usr/bin/env bash

script_name="try_KO_pre.r"
## Statement to get the max number of cpus on a machine
cpus=$( ls -d /sys/devices/system/cpu/cpu[[:digit:]]* | wc -w ) ## can CHANGE to an integer to set the max number of processes
## Function to make the number of CPUs match the number of processes
function pwait() {
	while [ $(ps -u | grep -v "grep" | grep -c "${script_name}") -ge $1 ]; do
        wait -n ## change to ""sleep 1"" if using bash version <4.3
    done
}

fps=('twoparam_0.00_0.40_asc_02_2' 'twoparam_0.00_0.40_asc_10_10' 'twoparam_0.20_0.80_asc_09_9' 'twoparam_0.20_0.80_asc_17_17' 'twoparam_0.20_1.00_asc_08_8' 'twoparam_0.40_0.60_asc_00_0' 'twoparam_0.40_0.60_asc_08_8' 'twoparam_0.40_0.60_asc_14_14' 'twoparam_0.40_0.60_asc_19_19' 'twoparam_0.40_1.00_asc_00_0' 'twoparam_0.40_1.00_asc_02_2' 'twoparam_0.40_1.00_asc_03_3' 'twoparam_0.40_1.00_asc_05_5' 'twoparam_0.40_1.00_asc_08_8' 'twoparam_0.40_1.00_asc_09_9' 'twoparam_0.40_1.00_asc_10_10' 'twoparam_0.40_1.00_asc_11_11' 'twoparam_0.40_1.00_asc_17_17' 'twoparam_0.80_1.00_asc_07_7' 'twoparam_0.80_1.00_asc_01_1' 'twoparam_0.60_1.00_asc_16_16' 'twoparam_0.40_1.00_asc_18_18' 'twoparam_0.40_1.00_asc_09_9')

in_list() {
    local search="$1"
    shift
    local list=("$@")
    for file in "${list[@]}" ; do
        [[ $file == $search ]] && return 0
    done
    return 1
}


ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
for ii in {00..19}; do
q1=1.00
printf -v i "%d" ${ii#0}
fp1=twoparam_${p}_${q1}_${order}_${ii}_${i}
if [ ! -f ./logging/${fp1}.txt ]; then
if in_list ${fp1} ${fps[@]}; then
echo ${fp1} "completed in simulation2.sh"
else
echo ${fp1}
nohup Rscript ${script_name} ${fp1} > ./logging/${fp1}.txt 2>&1 & 
pwait $cpus
fi
fi


q2=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q2}
fp2=twoparam_${p}_${q11}_${order}_${ii}_${i}
if [ ! -f ./logging/${fp2}.txt ]; then
if in_list ${fp2} ${fps[@]}; then
echo ${fp2} "completed in simulation2.sh"
else
echo ${fp2}
nohup Rscript ${script_name} ${fp2} > ./logging/${fp2}.txt 2>&1 & 
pwait $cpus
fi
fi

q3=0.00
fp3=twoparam_${q3}_${p}_${order}_${ii}_${i}
if [ ! -f ./logging/${fp3}.txt ]; then
if in_list ${fp3} ${fps[@]}; then
echo ${fp3} "completed in simulation2.sh"
else
echo ${fp3}
nohup Rscript ${script_name} ${fp3} > ./logging/${fp3}.txt 2>&1 & 
pwait $cpus
fi
fi
done

done
if [ ! -f ./logging/twoparam_1.00_0.00_${order}_00_0.txt ]; then
nohup Rscript ${script_name} twoparam_1.00_0.00_${order}_00_0 > ./logging/twoparam_1.00_0.00_${order}_00_0.txt 2>&1 &
pwait $cpus
fi

if [ ! -f ./logging/twoparam_0.00_1.00_${order}_00_0.txt ]; then
nohup Rscript ${script_name} twoparam_0.00_1.00_${order}_00_0 > ./logging/twoparam_0.00_1.00_${order}_00_0.txt 2>&1 &
pwait $cpus
fi

done
wait
