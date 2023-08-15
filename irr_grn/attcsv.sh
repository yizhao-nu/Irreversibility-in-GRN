ps=(0.20 0.40 0.60 0.80)
orders=('asc' 'desc')
for order in ${orders[@]}; do
for p in ${ps[@]}; do
for i in {0..9}; do
printf -v ii "%02d" ${i}
q1=1.00
printf -v ii "%02d" ${i}
nohup python3 att_csv.py ./netfiles/twoparam_${p}_${q1}_${order}_${ii}_${i} > ./attfiles/att_twoparam_${p}_${q1}_${order}_${ii}_${i}.txt 2>&1 & 
done
wait
for i in {0..9}; do
q1=$(bc -l <<<"1-${p}")
printf -v q11 "%.02f" ${q1}
printf -v ii "%02d" ${i}
nohup python3 att_csv.py ./netfiles/twoparam_${p}_${q11}_${order}_${ii}_${i}> ./attfiles/att_twoparam_${p}_${q11}_${order}_${ii}_{i}.txt 2>&1 & 
done
wait
done
nohup python3 att_csv.py ./netfiles/twoparam_0.00_1.00_${order}_00_1> ./attfiles/att_twoparam_0.00_1.00_${order}_00_1.txt 2>&1 &
nohup python3 att_csv.py ./netfiles/twoparam_0.00_0.00_${order}_00_1> ./attfiles/att_twoparam_0.00_1.00_${order}_00_1.txt 2>&1 &
nohup python3 att_csv.py ./netfiles/twoparam_1.00_1.00_${order}_00_1> ./attfiles/att_twoparam_1.00_1.00_${order}_00_1.txt 2>&1 &
done