#!/usr/bin/env bash
ps=(0.20 0.40 0.60 0.80)
ord=("asc" "desc")
for order in ${ord[@]}; do
    for p in ${ps[@]}; do
        q1=$(bc -l <<<"1-${p}")
        printf -v q11 "%.02f" ${q1}
        printf -v pp '%.02f' ${p}
        for i in {0..9}; do
            printf -v ii '%02d' ${i}
            ./bns "./netfiles/twoparam_${pp}_${q11}_${order}_${ii}_${i}.cnet" > "./attfiles/att_twoparam_${pp}_${q11}_${order}_${ii}_${i}.txt"
            ./bns "./netfiles/twoparam_${pp}_1.00_${order}_${ii}_${i}.cnet" > "./attfiles/att_twoparam_${pp}_1.00_${order}_${ii}_${i}.txt"
        done
        wait
    done
    #./bns "./netfiles/twoparam_0.00_1.00_${order}_00_1.cnet" > "./attfiles/att_twoparam_0.00_1.00_${order}_00_1.txt"
    #./bns "./netfiles/twoparam_0.00_0.00_${order}_00_1.cnet" > "./attfiles/att_twoparam_0.00_0.00_${order}_00_1.txt"
    #./bns "./netfiles/twoparam_1.00_1.00_${order}_00_1.cnet" > "./attfiles/att_twoparam_1.00_1.00_${order}_00_1.txt"
    wait
done
