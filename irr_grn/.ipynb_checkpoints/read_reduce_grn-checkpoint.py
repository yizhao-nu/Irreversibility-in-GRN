import networkx as nx
import pandas as pd
import numpy as np
import os

def read_in_network():
    fn = 'input_files/generegulation_tmp.txt'
    tab = pd.read_table(fn,skiprows=11,header=None)
    cols = []
    with open(fn,'r') as fh:
        ln = fh.readline().strip()
        while ln.startswith('#'):
            if ') ' in ln:
                cols.append(ln.split(') ')[1])
            ln = fh.readline().strip()
    tab.columns = cols
    return tab

def simplify(G):
    simplified_nodes = []
    for node in G.nodes:
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        if out_degree == 0:
            continue
        else:
            simplified_nodes.append(node)
    G_simplified = G.subgraph(simplified_nodes)
    print(len(simplified_nodes))
    return G_simplified

def main():
    df = read_in_network()
    df_sc = df.loc[:,['GENE_NAME_REGULATOR','GENE_NAME_REGULATED','GENEREGULATION_FUNCTION']]
    nodes = []
    edges = []
    sdef_edges = df_sc[df_sc.GENEREGULATION_FUNCTION.isin(['activator','repressor'])]
    G = nx.DiGraph()
    G.add_weighted_edges_from([(a,b,1 if c=='activator' else -1) for __,(a,b,c) in sdef_edges.iterrows()])
    #%%
    #sizes of strongly connected components
    sccs = sorted(nx.strongly_connected_components(G),key=len, reverse=True)
    wccs = sorted(nx.weakly_connected_components(G),key=len, reverse=True)
    len_sccs = [len(c) for c in sorted(nx.strongly_connected_components(G),key=len, reverse=True)]    
    len_wccs = [len(c) for c in sorted(nx.weakly_connected_components(G),key=len, reverse=True)] 

    #%%
    N = G.number_of_nodes()
    #shortest_path_lengths = np.zeros((num_nodes,num_nodes))
    nums_reached = {}
    nodes_reached = {}

    for uu in G.nodes:
        reached = [vv for vv in G.nodes if nx.has_path(G,uu,vv)]
        nums_reached[uu]=len(reached)
        nodes_reached[uu]=reached
    nums_reached_ser = pd.Series(nums_reached)
    nd_reached_most =nums_reached_ser.idxmax()
    reached_most = nodes_reached[nd_reached_most] + [nd_reached_most]
    G_wcc = G.subgraph(list(wccs[0]))
    G_reach = G.subgraph(reached_most)
    for ii,net in enumerate([G_reach,G_wcc]):
        LL = 1e10
        LLp = len(net.nodes)
        while LL > LLp:
            net = simplify(net)
            LL = LLp
            LLp = len(net.nodes)
        if ii==0:
            nx.write_gml('rs2.gml',net)
        else:
            pass
    
if __name__ == '__main__':
    main()