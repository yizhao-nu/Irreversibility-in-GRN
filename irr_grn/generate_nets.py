import networkx as nx
import numpy as np
import os,os.path as osp
import sys
import pandas as pd
import pyboolnet
from pyboolnet import file_exchange
rep = int(sys.argv[4])
RANDOM_SEED=rep
np.random.seed(RANDOM_SEED)

_path = os.path.dirname(os.path.realpath(__file__))

def truth_tables(G,p,q,order='asc'):
    truth_table_lines = ['targets, factors']
    degree = pd.Series(dict([(nd,dd) for nd,dd in G.out_degree]))
    reached = pd.Series(dict([(nd,len(nx.shortest_path(G,nd))) for nd in G.nodes]))
    asc = True if order=='asc' else False
    reached_sorted = pd.concat({'out_degree':degree,'total_descendants':reached},axis=1).sort_values(['out_degree','total_descendants'],ascending=asc)
    for node,row in reached_sorted.iterrows():
        truth_table = node+', '
        rand_in_edges = list(G.in_edges(node,data=True))
        rand_in_edges = sorted(rand_in_edges, key=lambda elt: reached_sorted.index.get_loc(elt[0]))
        if len(rand_in_edges) == 0:
            truth_table += node
        else:
            #randomly canalize = newneg2
            in_edge = rand_in_edges[0]

            if in_edge[2]['weight'] > 0:
                    truth_table += in_edge[0]
            else:
                if in_edge[1] == in_edge[0]:
                    truth_table += '(!'+in_edge[0]+'&'+in_edge[0] +')' #(!A&A)
                else:
                    truth_table += '!'+in_edge[0] #!A
            pts = 0
            p1 = p
            p2 = q
            #print('p and or: %s; p (: %s' % (p1,p2))
            for m in range(len(rand_in_edges)-1):
                in_edge = rand_in_edges[m+1]
                rand1 = np.random.random()
                if rand1 < p1:
                    truth_table += '& ('
                    pts += 1
                else:
                    rand2 = np.random.random()
                    if rand2 < p2:
                        truth_table += ' | '
                    else:
                        truth_table += ' & '
                    
                if in_edge[2]['weight'] > 0:
                    truth_table += in_edge[0]
                else:
                    if in_edge[1] == in_edge[0]:
                        truth_table += '(!'+in_edge[0]+'&'+in_edge[0] +')' #(!A&A) for auto-repression
                    else:
                        truth_table += '!'+in_edge[0] #!A for negative regulation                
            truth_table += ')'*(pts)
        truth_table_lines.append(truth_table)
    return truth_table_lines
    
def net(G,name,p,q,order):
    tt = truth_tables(G,p,q,order)
    with open(name+'.bnet','w+') as bnet:
        bnet.write('\n'.join(tt[1:]))
    
    with open(name+'.net','w+') as net:
        net.write('\n'.join(tt))
#"""
def cnet(name):
    primes = file_exchange.bnet2primes(name+'.bnet')
    cnet = file_exchange.primes2bns(primes)
    with open(name+'.cnet','w+') as net:
        net.write(cnet)
    
#"""
   
if __name__ == '__main__':
    cprob = float(sys.argv[1]) 
    bprob = float(sys.argv[2]) 
    order = sys.argv[3] 
    
    G_rs2 = nx.read_gml('./networks/rs2.gml')
    name = './netfiles/twoparam_%.2f_%.2f_%s_%02d_%d' % (cprob,bprob,order,rep,RANDOM_SEED)
    print(name)
    net(G_rs2,name,cprob,bprob,order)
    cnet(name)
    print("Done.")

