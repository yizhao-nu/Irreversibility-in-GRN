#!/usr/bin/env bash
ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
q1=1.00
for i in {00..19}; do
nohup python generate_nets.py ${p} ${q1} ${order} ${i}> netfiles/twoparam_${p}_${q1}_${order}_${i}.txt 2>&1 & 
done

wait

for i in {00..19}; do
q1=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q1}
nohup python generate_nets.py ${p} ${q11} ${order} ${i}> netfiles/twoparam_${p}_${q11}_${order}_${i}.txt 2>&1 & 
done

wait

done
nohup python generate_nets.py "0.00" "1.00" ${order} "00"> netfiles/twoparam_0.00_1.00_${order}_00.txt 2>&1 & 
nohup python generate_nets.py "1.00" "0.00" ${order} "00"> netfiles/twoparam_1.00_0.00_${order}_00.txt 2>&1 & 
done

