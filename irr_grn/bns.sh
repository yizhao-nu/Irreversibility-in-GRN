#!/usr/bin/env bash

cpus=8 ##$( ls -d /sys/devices/system/cpu/cpu[[:digit:]]* | wc -w ) ## can CHANGE to an integer to set the max number of processes
script_name="bns"
## Function to make the number of CPUs match the number of processes
function pwait() {
	while [ $(ps -u | grep -v "grep" | grep -c ${script_name}) -ge $1 ]; do
        wait -n ## change to ""sleep 1"" if using bash version <4.3
    done
}

ps=(0.20 0.40 0.60 0.80)
ord=("asc" "desc")
for order in ${ord[@]}; do
    for p in ${ps[@]}; do
        q1=$(bc -l <<<"1-${p}")
        printf -v q11 "%.02f" ${q1}
        printf -v pp '%.02f' ${p}
        for ii in {00..19}; do
            printf -v i '%d' "${ii#0}"
            ./${script_name} "./netfiles/twoparam_${pp}_${q11}_${order}_${ii}_${i}.cnet" > "./attfiles/att_twoparam_${pp}_${q11}_${order}_${ii}_${i}.txt" &
            ./${script_name} "./netfiles/twoparam_${pp}_1.00_${order}_${ii}_${i}.cnet" > "./attfiles/att_twoparam_${pp}_1.00_${order}_${ii}_${i}.txt" &
            ./${script_name} "./netfiles/twoparam_0.00_${pp}_${order}_${ii}_${i}.cnet" > "./attfiles/att_twoparam_0.00_${pp}_${order}_${ii}_${i}.txt" &
            pwait ${cpus}
        done
    done
    ./${script_name} "./netfiles/twoparam_0.00_1.00_${order}_00_0.cnet" > "./attfiles/att_twoparam_0.00_1.00_${order}_00_0.txt" &
    ./${script_name} "./netfiles/twoparam_1.00_0.00_${order}_00_0.cnet" > "./attfiles/att_twoparam_0.00_0.00_${order}_00_0.txt" &
    pwait ${cpus}
done
