#!/usr/bin/env bash
ps=(0.2 0.4 0.6 0.8)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
for i in {0..9}; do
nohup python3 generate_nets.py ${p} ${order} ${i}> gennet_${p}_${order}_${i}.txt 2>&1 & 
done
done
nohup python3 generate_nets.py 0 ${order} 0> gennet_${p}_${order}_${i}.txt 2>&1 & 
nohup python3 generate_nets.py 1 ${order} 0> gennet_${p}_${order}_${i}.txt 2>&1 & 
done
