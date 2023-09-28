# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 20:47:26 2020

@author: Yi Zhao
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



def merge_dict(x,y):
    for k,v in x.items():
        if k in y.keys():
            y[k] += v
        else:
            y[k] = v
gene_name = 'crp'
for type_network in ['so']:                   
    counts_total = {}
    response_nodes = set()
    ps = [0,0.2,0.4,0.6,0.8]
    exps = []
    names = []
    for prob in ps:
        for i in range(5):
            #name = r'/data/yizhao/irr/result/changed/summary-'+gene_name+'-newcan2_rs2_'+str(prob)+'_'+type_network+'_'+str(i)+'-ng2-.csv'
            #name = r'/data/yizhao/irr/result/changed/summary-'+gene_name+'-newneg2_rs2_'+str(prob)+'_'+type_network+'_'+str(i)+'-ng2-.csv'
            name = r'/data/yizhao/irr/result/changed/summary-'+gene_name+'-rs2_'+str(prob)+'_'+type_network+'_'+str(i)+'-ng2-.csv'
            names.append(name)
            exps.append(str(prob)+'-'+str(i))
    exps.append('1')
    #names.append(r'/data/yizhao/irr/result/changed/summary-'+gene_name+'-newcan2_rs2_f_'+type_network+'-ng2-.csv')
    #names.append(r'/data/yizhao/irr/result/changed/summary-'+gene_name+'-newneg2_rs2_f_'+type_network+'-ng2-.csv')
    for name in names:
        f = open(name,'r',encoding='utf-8')
        reader = csv.reader(f)
        re = np.array(list(reader))
        result = np.array(re[1:,1:])
        nodes = re[0,1:]
        N = result.shape[1]
        exp = result.shape[0]
        final = result[0,:]
        
        #print(nodes)
        
        #print(nodes[:np.where(final=='0')[0][0]])
        
        #print(final[:np.where(final=='0')[0][0]])
        

        response_node = set(nodes[:np.where(final=='0')[0][0]])

        response_nodes = response_nodes | response_node
    response_nodes = list(response_nodes)
    
    print(response_nodes)

    total1 = []
    total2 = []
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
        by_2 = result[0,:]
        
        at_1 = result[1,:]
        changed_by_2_dict = dict(zip(nodes,by_2))
        changed_at_1_dict = dict(zip(nodes,at_1))

        row_by_2 = []
        row_at_1 = []

        for response_node in response_nodes:

            elm_by_2 = float(changed_by_2_dict[response_node])
            elm_at_1 = float(changed_at_1_dict[response_node])


            row_by_2.append(elm_by_2)
            row_at_1.append(elm_at_1)


        total2.append(row_by_2)
        total1.append(row_at_1)


    data = np.array(total2)
    print(data.shape)
    
    data_mean = np.mean(data,axis = 0)
    data_std = np.std(data,axis = 0)
    data1 = np.array(total1)
    data1_mean = np.mean(data1,axis = 0)
    data1_std = np.std(data1,axis = 0)
    
    data_summary = np.vstack((data_mean,data_std,data1_mean,data1_std))

    import pandas as pd
    

    df=pd.DataFrame(data,columns=response_nodes,index=exps)
    print(df)
    df.to_csv('df_total_by_2_org_'+gene_name+'_'+type_network+'.csv')

    df1=pd.DataFrame(data1,columns=response_nodes,index=exps)
    print(df1)
    df1.to_csv('df_total_at_1_org_'+gene_name+'_'+type_network+'.csv')

    df2 = pd.DataFrame(data_summary,columns=response_nodes,index=['mean changed by 2','std changed by 2','mean changed at 1','std changed at 1'])
    df2.to_csv('df_summary_org_'+gene_name+'_'+type_network+'.csv')
#plt.plot()

#ax = sns.heatmap(df,mask=(df==0),xticklabels=True, yticklabels=True)
#ax.set_facecolor("gray")
#plt.savefig('heatmap_'+type_pert+'_'+type_network+'.png',dpi=300)


        
        
        
        