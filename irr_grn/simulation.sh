#!/usr/bin/env bash

ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
for i in {00..09}; do
nohup Rscript try_KO_pre.r newneg2_rs2_${p}_${order}_${i}_1> newneg2_rs2_${p}_${order}_${i}.txt 2>&1 & 
done
done
nohup Rscript try_KO_pre.r newneg2_rs2_0.00_${order}_00_1> newneg2_rs2_0_${order}_0.txt 2>&1 &
nohup Rscript try_KO_pre.r newneg2_rs2_1.00_${order}_00_1> newneg2_rs2_1_${order}_0.txt 2>&1 &
done