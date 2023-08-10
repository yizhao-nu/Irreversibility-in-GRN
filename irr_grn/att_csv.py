# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 00:37:36 2021

@author: 赵诣
"""
import sys
import numpy as np

def nodes_from_bnet(txt_name):
    
    fo=open(txt_name+'.bnet',encoding='utf-8') #read texts
    p=fo.readlines()
    nodes = []
    for line in p:
        line = line.split(',')
        nodes.append(line[0])
    return np.array(nodes)
def nodes_from_cnet(txt_name):
    
    fo=open(txt_name+'.cnet',encoding='utf-8') #read texts
    p=fo.readlines()[0]
    p = p.strip().replace('\n', "")
    p = p.strip().replace('#', "")
    p = p.strip()       
    
    line = p.split(', ')
    
    nodes = line
    return np.array(nodes)

def get_element_index(ob_list, word_list):
    idx_list = []
    for word in word_list:
        idx = [i for (i, v) in enumerate(ob_list) if v == word]
        idx_list+=idx
    idx_list = list(idx_list)
    idx_list = np.array(list(idx_list),dtype=int)
    return idx_list

def attractors_1state_from_txt(txt_name, network_name, cleanup=True):

    nodes_bnet = nodes_from_bnet(network_name)
    nodes_cnet = nodes_from_cnet(network_name)
    idx = get_element_index(nodes_cnet,nodes_bnet)
    print(nodes_bnet)
    print(nodes_cnet[idx])
   
    
    attractors = list()

	
    fo=open(txt_name+'.txt',encoding='utf-8') #read texts
    p=fo.readlines()

    current_attractor = []
    sizes = []
    for i,line in enumerate(p):
        # Strip line
        cleanline = line.strip().replace('\n', "")
        #print("{:d}: '{:s}'".format(i ,cleanline))
			
        if 'Attractor' in cleanline:
            attractors.append(current_attractor[0])
            current_attractor = []
            size = cleanline[-1]
            
            sizes.append(size)
        elif 'nohup' in cleanline:
            pass    
        elif 'Node' in cleanline and 'assumed to be constant' in cleanline:
            pass
        elif 'Total' in cleanline:
            pass
        elif 'Start searching for all atractors.' in cleanline:
            pass
        elif 'Depth' in cleanline:
            pass
        elif 'average' in cleanline:
            pass
        elif len(cleanline) > 0:
            #current_attractor.append( binstate_to_statenum(cleanline) )
            
            cleanline = list(cleanline)
            cleanline = np.array(list(map(int, cleanline)))
            current_attractor.append(cleanline)

    attractors = np.array(attractors).astype(int)[:,idx]
    np.savetxt('./attfiles/1st'+txtname.split(r'/')[2][4:]+'.csv', attractors, delimiter = ',') 
    return attractors    

    

txtname = sys.argv[1] 
networkname = './netfiles/'+txtname.split(r'/')[2][4:]
#name = 'att_newneg2_0.2_so_5'#'att_newneg2_0_so_6'
atts = attractors_1state_from_txt(txtname, networkname)#'newneg2_rs2_0_so_6')

print(atts.shape)
#np.savetxt('./attfiles/1st'+txtname.split(r'/')[2][4:]+'.csv', atts, delimiter = ',') 


