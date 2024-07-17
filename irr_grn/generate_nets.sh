#!/usr/bin/env bash

cpus=8 ##$( ls -d /sys/devices/system/cpu/cpu[[:digit:]]* | wc -w ) ## can CHANGE to an integer to set the max number of processes
script_name="generate_nets.py"
## Function to make the number of CPUs match the number of processes
function pwait() {
	while [ $(ps -u | grep -v "grep" | grep -c ${script_name}) -ge $1 ]; do
        wait -n ## change to ""sleep 1"" if using bash version <4.3
    done
}


ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
q1=1.00
for i in {00..19}; do
nohup python ${script_name} ${p} ${q1} ${order} ${i}> netfiles/twoparam_${p}_${q1}_${order}_${i}.txt 2>&1 &
pwait ${cpus}
done

for i in {00..19}; do
q1=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q1}
nohup python ${script_name} ${p} ${q11} ${order} ${i}> netfiles/twoparam_${p}_${q11}_${order}_${i}.txt 2>&1 &
pwait ${cpus}
done

for i in {00..19}; do
q1=0
printf -v q11 "%.02f" ${q1}
nohup python ${script_name} ${q11} ${p} ${order} ${i}> netfiles/twoparam_${q11}_${p}_${order}_${i}.txt 2>&1 & 
pwait ${cpus}
done


done
nohup python ${script_name} "0.00" "1.00" ${order} "00"> netfiles/twoparam_0.00_1.00_${order}_00.txt 2>&1 & 
nohup python ${script_name} "1.00" "0.00" ${order} "00"> netfiles/twoparam_1.00_0.00_${order}_00.txt 2>&1 &
pwait ${cpus}
done

