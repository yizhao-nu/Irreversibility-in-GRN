import networkx as nx
import re
import xlwt
import xlrd
from tqdm import tqdm
import numpy as np
import os
from tqdm import tqdm
import pyboolnet
from pyboolnet import file_exchange
import os
import subprocess
import tempfile
import numpy as np


_path = os.path.dirname(os.path.realpath(__file__))

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
def truth_tables(Graph,metrics,p):
    if metrics == 'yaml':
        truth_tables = ['update rules:']
        for node in Graph.nodes:
          
            truth_table = '\n    '+node+': '
            pos_in_edges = [e for e in Graph.in_edges(node,data=True) if e[2]['weight']>0]
            neg_in_edges = [e for e in Graph.in_edges(node,data=True) if e[2]['weight']<0]
           
            if len(pos_in_edges)+len(neg_in_edges) == 0:
                truth_table = '\n    '+node+': '+node
            else:
                if len(pos_in_edges)>0:   
                    for m in range(len(pos_in_edges)):
                        in_edge = pos_in_edges[m]
                        if m == 0:
                            truth_table += '('+in_edge[0]
                        else:
                            truth_table += ' or '+in_edge[0]
                    truth_table += ')'
                                
                if len(neg_in_edges)>0:
                    if len(pos_in_edges)!=0 and len(neg_in_edges)!=0:
                        truth_table += ' and '
                    
                    for n in range(len(neg_in_edges)):
                        in_edge = neg_in_edges[n]
                        if n == 0:
                            truth_table += '(not '+in_edge[0]
                        else:
                            truth_table += ' and not '+in_edge[0]
                    truth_table += ')'
               
            truth_tables.append(truth_table)
            #print(truth_table)
            #d
    if metrics == 'net':
        truth_tables = ['targets, factors']
        degree = Graph.out_degree
        degree = [i[1] for i in degree]
        reached = list(zip(Graph.nodes, num_reachable(Graph,Graph.nodes),degree))
        #reached_sorted = sorted(reached, key=lambda elem: (-elem[1], -elem[2])) #so
        reached_sorted = sorted(reached, key=lambda elem: (elem[1], elem[2])) #inv
        Map = {c[0]: i for i, c in enumerate(reached_sorted)}
        for node in Graph.nodes:
            truth_table = '\n'+node+', '
            pos_in_edges = [e for e in Graph.in_edges(node,data=True) if e[2]['weight']>0]
            pos_in_edges = sorted(pos_in_edges, key=lambda tup: Map.get(tup[0], -1))
            neg_in_edges = [e for e in Graph.in_edges(node,data=True) if e[2]['weight']<0]
            neg_in_edges = sorted(neg_in_edges, key=lambda tup: Map.get(tup[0], -1))
            rand_in_edges = list(Graph.in_edges(node,data=True))
            #print(rand_in_edges)
            
            rand_in_edges = sorted(rand_in_edges, key=lambda tup: Map.get(tup[0], 0))
            
            #np.random.shuffle(rand_in_edges)
         
            if len(pos_in_edges)+len(neg_in_edges) == 0:
                truth_table += node
            else:
                #randomly canalize = newneg2
                in_edge = rand_in_edges[0]
                
                #print(len(rand_in_edges))
                
                if in_edge[2]['weight'] > 0:
                        truth_table += in_edge[0]
                else:
                    if in_edge[1] == in_edge[0]:
                        truth_table += '(!'+in_edge[0]+'&'+in_edge[0] +')' #(!A&A)
                    else:
                        truth_table += '!'+in_edge[0] #!A
                
                pts = 0
                p1 = p #np.random.random()
                p2 = 0 #np.random.random()
                p3 = 0.5
                #print('p and or: %s; p (: %s' % (p1,p2))
                for m in range(len(rand_in_edges)-1):
                    in_edge = rand_in_edges[m+1]
                    rand1 = int(np.random.binomial(1, p1, 1))
                    rand2 = int(np.random.binomial(1, p2, 1))
                    rand3 = int(np.random.binomial(1, p3, 1))
                    if rand1 == 1:
                        truth_table += '|('
                    elif rand1 == 0:
                        if rand2 == 0:
                            truth_table += '|'
                            pts += 1
                        elif rand2 == 1:
                            truth_table += '&'
                            if rand3 == 0:
                                truth_table += '('
                            elif rand3 ==1:
                                pts += 1
                    if in_edge[2]['weight'] > 0:
                            truth_table += in_edge[0]
                    else:
                        if in_edge[1] == in_edge[0]:
                            truth_table += '(!'+in_edge[0]+'&'+in_edge[0] +')' #(!A&A) for auto-repression
                        else:
                            truth_table += '!'+in_edge[0] #!A for negative regulation
                
                truth_table += ')'*(len(rand_in_edges)-pts-1)
                
            truth_tables.append(truth_table)
            #print(truth_tables)
            
    
    return truth_tables
def nodes(Graph):
    txts = ['nodes:']
    for node in Graph.nodes:
        txt = '\n- '+node
        txts.append(txt)
    return txts
def initial_state(Graph):
    txts = ['initial state:']
    for node in Graph.nodes:
        txt = '\n    '+node+': any'
        txts.append(txt)
    return txts
def yaml(Graph,name):
    yaml = open(name+'.yaml','w+')
    l = []
    yaml_nodes = nodes(Graph)
    yaml_update_rules = truth_tables(Graph,'yaml')
    yaml_initial_state = initial_state(Graph)
    l = yaml_nodes+['\n']+yaml_update_rules+['\n']+yaml_initial_state
    yaml.writelines(l)
    yaml.close()     
def net(Graph,name,p):
    bnet = open(name+'.bnet','w+')
    tt = truth_tables(Graph,'net',p)
    bnet.writelines(tt[1:])
    bnet.close()
    net = open(name+'.net','w+')
    net.writelines(tt)
    net.close()
#"""
def cnet(name):
    primes = file_exchange.bnet2primes(name+'.bnet')
    cnet = file_exchange.primes2bns(primes)
    net = open(name+'.cnet','w+')
    net.write(cnet)
    net.close()
#"""
def nodes_from_bnet(txt_name):
    
    fo=open(txt_name+'.bnet',encoding='utf-8') #read texts
    p=fo.readlines()
    nodes = []
    for line in p[1:]:
        line = line.split(',')
        nodes.append(line[0])
    return nodes
def nodes_from_cnet(txt_name):
    
    fo=open(txt_name+'.cnet',encoding='utf-8') #read texts
    p=fo.readlines()
    nodes = []
    for line in p[1:]:
        line = line.split(',')
        nodes.append(line[0])
    return nodes

def get_element_index(ob_list, word_list):
    idx_list = []
    for word in word_list:
        idx = [i for (i, v) in enumerate(ob_list) if v == word]
        idx_list+=idx
    idx_list = list(idx_list)
    idx_list = np.array(list(idx_list))
    return idx_list

   

G_rs2 = nx.read_gml('./networks/rs2.gml')
ps = [0,0.2,0.4,0.6,0.8]

for prob in ps:
    for i in range(10):
        name = './netfiles/newneg2_rs2_'+str(prob)+'_so_'+str(i)
        print(name)
        cnet(name)


#G_rs2 = nx.read_gml('rs2.gml')
#name = 'newcan2_rs2_f_so'
#net(G_rs2,name,p=1)
#"""