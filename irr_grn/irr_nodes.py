# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 20:47:26 2020

@author: 赵诣
"""
import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt

def num_reachable(G,group):
    # input: nx.Graph G & group of nodes (list or set)
    # output: a list of nodes reaching to the given group starting with the original group
    nums_reached = []
    nodes_reached = []
    set_reached = set()
    N = G.number_of_nodes()
    nodes = list(G.nodes())
    group = list(group)
    for j in range(len(group)):
        num_reached = N
        nodes_reaching_to_j = list(np.array(nodes))
        for k in range(N):
            try:
                length=nx.shortest_path_length(G,source=group[j],target=nodes[k])
            except nx.NetworkXNoPath:
                num_reached -= 1
        nums_reached.append(num_reached)
    return nums_reached 
G_rs2 = nx.read_gml('rs2.gml')
degree = G_rs2.out_degree
degree = [i[1] for i in degree]
reached = list(zip(G_rs2.nodes, degree,num_reachable(G_rs2,G_rs2.nodes),))
reached = sorted(reached, key=lambda elem: (-elem[1], -elem[2]))
Map = {c[0]: i for i, c in enumerate(reached)}

def merge_dict(x,y):
    for k,v in x.items():
        if k in y.keys():
            y[k] += v
        else:
            y[k] = v
                    
type_network = 'so'
type_pert = 'OE'
counts_total = {}
irr_nodes = set()
ps = [0,0.2,0.4,0.6,0.8]
exps = []
names = []
for prob in ps:
    for i in range(10):
        name = r'/data/yizhao/irr/result/result-'+type_pert+'-1e4-newneg2_rs2_'+str(prob)+'_'+type_network+'_'+str(i)+'-pre-.csv'
        names.append(name)
        exps.append(str(prob)+'-'+str(i))
exps.append('1')
names.append(r'/data/yizhao/irr/result/result-'+type_pert+'-1e4-newneg2_rs2_f_'+type_network+'-pre-.csv')
for name in names:
    f = open(name,'r',encoding='utf-8')
    reader = csv.reader(f)
    re = np.array(list(reader))
    result = np.array(re[1:,1:])
    nodes = re[0,1:]
    N = result.shape[1]
    exp = result.shape[0]
    final = result[-2,:]
    #print(nodes)
    #print(final)
    #print(nodes[:np.where(final=='0')[0][0]])
    #print(final[:np.where(final=='0')[0][0]])
    
    irr_node = set(nodes[:np.where(final=='0')[0][0]])
    
    irr_nodes = irr_nodes | irr_node
irr_nodes = list(irr_nodes)
irr_nodes = sorted(irr_nodes, key=lambda elem: Map.get(elem, -1))

total = []
total_noNA = []
states = []
#for prob in ps:
for name in names:
    
    f = open(name,'r',encoding='utf-8')
    reader = csv.reader(f)
    re = np.array(list(reader))
    nodes = re[0,1:]
    result = np.array(re[1:,1:])
    """
    N = result.shape[1]
    new_result = []
    
    for i in range(result.shape[0]):
        row = result[i,:]
        if str(row) != str(np.array(['NA']*N)):
            new_result.append(row)
    new_result = np.array(new_result)
    exp = new_result.shape[0]-1
    print(exp)
    """
    final = result[-2,:]
    count_dict = dict(zip(nodes,final))
    state_dict = dict(zip(nodes,result[-1,:]))
    
    row = []
    row_noNA = []
    row_state = []
    for irr_node in irr_nodes:
        #count = float(count_dict[irr_node])
        #perct = count/exp
        #row.append(perct)
        elm = count_dict[irr_node]
        elm_noNA = count_dict[irr_node]
        if elm_noNA == 'NA':
            elm_noNA = 0
        elm_noNA = float(elm_noNA)
        elm = float(elm_noNA)
        row.append(elm)
        row_noNA.append(elm_noNA)
        row_state.append(state_dict[irr_node])
    
    total.append(row)
    total_noNA.append(row_noNA)
    states.append(row_state)

data = np.array(total)
data1 = np.array(total_noNA)
states = np.array(states)
import pandas as pd
import seaborn as sns

df=pd.DataFrame(data,columns=irr_nodes,index=exps)
print(df)
df.to_csv('df_neg2_pre'+type_pert+'_'+type_network+'.csv')

df1=pd.DataFrame(data1,columns=irr_nodes,index=exps)
print(df1)
df1.to_csv('df_neg2_pre_noNA_'+type_pert+'_'+type_network+'.csv')

df2 = pd.DataFrame(states,columns=irr_nodes,index=exps)
df2.to_csv('states_neg2_pre_'+type_pert+'_'+type_network+'.csv')
#plt.plot()

#ax = sns.heatmap(df,mask=(df==0),xticklabels=True, yticklabels=True)
#ax.set_facecolor("gray")
#plt.savefig('heatmap_'+type_pert+'_'+type_network+'.png',dpi=300)


        
        
        
        