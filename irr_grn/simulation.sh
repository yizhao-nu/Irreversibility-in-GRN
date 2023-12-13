#!/usr/bin/env bash

## Statement to get the max number of cpus on a machine
cpus=$( ls -d /sys/devices/system/cpu/cpu[[:digit:]]* | wc -w ) ## can CHANGE to an integer to set the max number of processes
## Function to make the number of CPUs match the number of processes
function pwait() {
	while [ $(ps -u | grep -v "grep" | grep -c "try_KO_pre.r") -ge $1 ]; do
        wait -n ## change to ""sleep 1"" if using bash version <4.3
    done
}

ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
for ii in {00..19}; do
q1=1.00
printf -v i "%d" ${ii#0}
if [ ! -f ./logging/twoparam_${p}_${q1}_${order}_${ii}_${i}.txt ]; then
echo ${p}_${q1}_${order}_${ii}_${i}
nohup Rscript try_KO_pre.r twoparam_${p}_${q1}_${order}_${ii}_${i} > ./logging/twoparam_${p}_${q1}_${order}_${ii}_${i}.txt 2>&1 & 
pwait $cpus
fi


q2=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q2}
if [ ! -f ./logging/twoparam_${p}_${q11}_${order}_${ii}_${i}.txt ]; then
echo ${p}_${q11}_${order}_${ii}_${i}
nohup Rscript try_KO_pre.r twoparam_${p}_${q11}_${order}_${ii}_${i} > ./logging/twoparam_${p}_${q11}_${order}_${ii}_${i}.txt 2>&1 & 
pwait $cpus
fi

q3=0.00
if [ ! -f ./logging/twoparam_${q3}_${p}_${order}_${ii}_${i}.txt ]; then
echo ${q3}_${p}_${order}_${ii}_${i}
nohup Rscript try_KO_pre.r twoparam_${q3}_${p}_${order}_${ii}_${i} > ./logging/twoparam_${q3}_${p}_${order}_${ii}_${i}.txt 2>&1 & 
pwait $cpus
fi
done

done
if [ ! -f ./logging/twoparam_1.00_0.00_${order}_00_0.txt ]; then
nohup Rscript try_KO_pre.r twoparam_1.00_0.00_${order}_00_0 > ./logging/twoparam_1.00_0.00_${order}_00_0.txt 2>&1 &
pwait $cpus
fi

if [ ! -f ./logging/twoparam_0.00_1.00_${order}_00_0.txt ]; then
nohup Rscript try_KO_pre.r twoparam_0.00_1.00_${order}_00_0 > ./logging/twoparam_0.00_1.00_${order}_00_0.txt 2>&1 &
pwait $cpus
fi

done
wait
