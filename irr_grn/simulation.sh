#!/usr/bin/env bash

ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
for ii in {00..19}; do
q1=1.00
printf -v i "%d" ${ii#0}
nohup Rscript try_KO_pre.r twoparam_${p}_${q1}_${order}_${ii}_${i}> ./results/twoparam_${p}_${q1}_${order}_${ii}_${i}.txt 2>&1 & 
done
wait
for ii in {00..19}; do
q2=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q2}
nohup Rscript try_KO_pre.r twoparam_${p}_${q11}_${order}_${ii}_${i}> ./results/twoparam_${p}_${q11}_${order}_${ii}_${i}.txt 2>&1 & 
done
wait
for ii in {00..19}; do
q3=0.00
nohup Rscript try_KO_pre.r twoparam_${q3}_${p}_${order}_${ii}_${i} > ./attfiles/att_twoparam_${q3}_${p}_${order}_${ii}_${i}.txt 2>&1 & 
done
wait
done
nohup Rscript try_KO_pre.r twoparam_1.00_0.00_${order}_00_0> ./results/twoparam_1.00_0.00_${order}_00_0.txt 2>&1 &
nohup Rscript try_KO_pre.r twoparam_0.00_1.00_${order}_00_0> ./results/twoparam_0.00_1.00_${order}_00_0.txt 2>&1 &
done