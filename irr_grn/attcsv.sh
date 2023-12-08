ps=(0.20 0.40 0.60 0.80)
ord=('asc' 'desc')
for order in ${ord[@]}; do
for p in ${ps[@]}; do
for ii in {00..19}; do
q1=1.00
printf -v i "%d" ${ii#0}
nohup python att_csv.py ./netfiles/twoparam_${p}_${q1}_${order}_${ii}_${i} > ./attfiles/1stOP_twoparam_${p}_${q1}_${order}_${ii}_${i}.txt 2>&1 & 

q2=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q2}
nohup python att_csv.py ./netfiles/twoparam_${p}_${q11}_${order}_${ii}_${i}> ./attfiles/1stOP_twoparam_${p}_${q11}_${order}_${ii}_${i}.txt 2>&1 & 

q3=0.00
nohup python att_csv.py ./netfiles/twoparam_${q3}_${p}_${order}_${ii}_${i} > ./attfiles/1stOP_twoparam_${q3}_${p}_${order}_${ii}_${i}.txt 2>&1 & 
done
wait

done
nohup python att_csv.py ./netfiles/twoparam_0.00_1.00_${order}_00_0> ./attfiles/1stOP_twoparam_0.00_1.00_${order}_00_0.txt 2>&1 &
nohup python att_csv.py ./netfiles/twoparam_1.00_0.00_${order}_00_0> ./attfiles/1stOP_twoparam_1.00_0.00_${order}_00_0.txt 2>&1 &
done