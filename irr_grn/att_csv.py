# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 00:37:36 2021

@author: 赵诣
@author2: Thomas P. Wytock
"""
import sys
import numpy as np
import pandas as pd

def attractors_1state_from_txt(txt_name, network_name, cleanup=True):
    with open(network_name+'.bnet',encoding='utf-8') as fo:
        nodes_bnet = [ln.strip().split(',')[0] for ln in fo]
    with open(network_name+'.cnet',encoding='utf-8') as fo:
        ln0=fo.readline()
    ln0 = ln0.replace('\n', "").replace('#', "").strip()
    nodes_cnet = ln0.split(', ')
    idx = pd.Series(dict([(vv,kk) for kk,vv in enumerate(nodes_cnet)])).loc[nodes_bnet]
    attractors = list()
    with open(txt_name,encoding='utf-8') as fo:
        p=fo.readlines()
    current_attractor = []
    sizes = []
    for line in p[1:]:
        # Strip line
        cleanline = line.strip().replace('\n', "")
        #print("{:d}: '{:s}'".format(i ,cleanline))
        if cleanline.startswith('Attractor'):
            attractors.append(current_attractor[0])
            current_attractor = []
            size = cleanline[-1]            
            sizes.append(size)
        elif 'average' in cleanline:
            pass
        elif len(cleanline) > 0 and cleanline.startswith(('0','1')):
            cleanline = np.array([int(elt) for elt in cleanline])
            current_attractor.append(cleanline)

    attractors = np.c_[attractors].astype(int)[:,idx.values]
    np.savetxt('./attfiles/1st_%s.csv' % (network_name.split('/')[-1]), attractors, delimiter = ',') 
    return attractors    

    
if __name__=='__main__':
    network_name = sys.argv[1] 
    att_name = './attfiles/att_%s.txt' % network_name.split(r'/')[2]
    atts = attractors_1state_from_txt(att_name, network_name)


