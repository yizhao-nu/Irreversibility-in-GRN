#!/usr/bin/env bash
ps=(0.20 0.40 0.60 0.80)
ord=("asc" "desc")
for o in ${ord[@]} do
    for p in ${ps[@]}; do
        for i in {0..9}; do
            printf -v ii '%2d' i
            printf -v pp '%.2f' p
            nohup ./bns ./netfiles/newneg2_rs2_${pp}_${o}_${ii}_1.cnet> ./attfiles/att_newneg2_rs2_${pp}_${o}_${ii}_1.txt 2>&1 & 
    done
    nohup ./bns ./netfiles/newneg2_rs2_0.00_${o}_00_1.cnet> ./attfiles/att_newneg2_rs2_0.00_${o}_00_1.txt 2>&1 &
    nohup ./bns ./netfiles/newneg2_rs2_1.00_${o}_00_1.cnet> ./attfiles/att_newneg2_rs2_1.00_${o}_00_1.txt 2>&1 &
done

