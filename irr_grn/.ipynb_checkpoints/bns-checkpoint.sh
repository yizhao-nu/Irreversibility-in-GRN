#!/usr/bin/env bash
ps=(0.20 0.40 0.60 0.80)
for p in ${ps[@]}; do
    for i in {0..9}; do
        ./bns newneg2_rs2_${p}_inv_${i}.cnet> att_newneg2_rs2_${p}_so_${i}.txt 2>&1 & 
    done
done

nohup ./bns newneg2_rs2_0.00_inv.cnet> att_newneg2_rs2_f_inv.txt 2>&1 &
nohup ./bns newneg2_rs2_1.00_inv.cnet> att_newneg2_rs2_f_inv.txt 2>&1 &
