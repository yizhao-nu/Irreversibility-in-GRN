
"""attractor_weighted_irreversibility.py

author: Thomas P. Wytock
author2: Yi Zhou
date: 04/05/2024
"""

import numpy as np
import pickle as P
import networkx as nx
import pandas as pd
from itertools import combinations as combs
from functools import partial
from scoop import futures
from matplotlib import pyplot as plt
np.set_printoptions(threshold=20)
import os.path as osp
import sys

def calc_attr_weight_boltz(a0_a1_it,b0_b1,act_probs,beta=1):
    lbl,(a0,a1) = a0_a1_it
    b0,b1 = b0_b1
    tot = 0
    for pair in [(a0.values,b0.values),(a1.values,b1.values)]:
        for ii in range(a0.shape[0]):
            ai = pair[0][ii]
            bi = pair[1][ii]
            p_i = act_probs.iloc[ii]
            sgn = -1 if ai==bi else 1
            qi = p_i if bi==1 else 1-p_i
            tot+=sgn*np.log(qi)
    return lbl,np.exp(beta*tot)

def calc_attr_weight_hamming(a0_a1_it,b0_b1,beta=1):
    lbl,(a0,a1) = a0_a1_it
    b0,b1 = b0_b1
    H = (a0!=b0).sum()+(a1!=b1).sum()
    return lbl,H,np.exp(-1*beta*H)
    
bpj_tup_d = {'PRJNA638644':[{'OFF':[1973, 1974],'ON':[1971,1972]},
                            {'OFF':[1987, 1988],'ON':[1985,1986]}],
             'PRJNA272157':[{'ON':[1892,1893],'OFF':[1889,1890]},
                            {'ON':[1892,1893],'OFF':[1884,1885,1886]},
                            {'ON':[1889,1890],'OFF':[1881,1882,1883]},
                            {'ON':[1887,1888],'OFF':[1878,1879,1880]}],
             'PRJNA412866':[{'OFF':[2290,2291],'ON':[2298,2299]},
                            {'OFF':[2294,2295],'ON':[2292,2293]},
                            {'OFF':[2296,2297],'ON':[2298,2299]},
                            {'OFF':[2280,2281],'ON':[2288,2289]},
                            {'OFF':[2286,2287],'ON':[2288,2289]},
                            {'OFF':[2284,2285],'ON':[2282,2283]}],
             'PRJNA656833':[{'ON':[3207,3208,3209],'OFF':[3222,3223,3224]},
                            {'OFF':[3207,3208,3209],'ON':[3210,3211,3212]}],
             'PRJNA324683':[{'ON':[1910,1911],'OFF':[1896,1897]}],
             'PRJNA836545':[{'ON':[2275,2279],'OFF':[2273,2274]}],
            }

def main(mdrow2col_v,binstates_df,gsym_bias_ser,sb=True):
    ss_rr_pairs = [(1,0),(0,1),(0,0.8),(0,0.6),(0,0.4),(0,0.2),(0.2,0.8),(0.2,1),
                   (0.4,0.6),(0.4,1),(0.6,0.4),(0.6,1),(0.8,0.2),(0.8,1)]
    a1str = 'a1-irrgn'
    irrstr = 'irrev-changed'
    revstr = 'rev-changed'
                                
    boltz_summaries = {}
    hamming_summaries = {}
    wts_summaries = {}
    if isinstance(sb,bool):
        ext=''
    elif isinstance(sb,str):
        ext=f'_{sb}'
    else:
        print(f'Unknown extention: {sb}')
        raise

    if not osp.exists('results/crp/attractor_args_d.pkl'):
        ## for all combinations of attractors (across all files), 
        gene_status_d = {}
        attractor_args_d = {}
        ## collect all attractors
        for oord in ['asc','desc']:
            print(oord)
            for ss,rr in ss_rr_pairs:
                print(ss,rr)
                max_rep = 1 if (ss==1 and rr==0) or (ss==0 and rr==1) else 20
                for rep in range(max_rep):
                    print(rep)
                    a1fn = f'results/crp/{a1str}-KO-twoparam_{ss:.2f}_{rr:.2f}_{oord}_{rep:02d}_{rep:d}-crp.csv'
                    a1_states = pd.read_csv(a1fn,index_col=0)
                    irrfn = f'results/crp/{irrstr}-KO-twoparam_{ss:.2f}_{rr:.2f}_{oord}_{rep:02d}_{rep:d}-pre.csv'
                    irr_gns = pd.read_csv(irrfn,index_col=0)
                    revfn = f'results/crp/{revstr}-KO-twoparam_{ss:.2f}_{rr:.2f}_{oord}_{rep:02d}_{rep:d}-pre.csv'
                    rev_gns = pd.read_csv(revfn,index_col=0)
                    attfn = f'attfiles/1st_twoparam_{ss:.2f}_{rr:.2f}_{oord}_{rep:02d}_{rep:d}.csv'
                    attdat = pd.read_csv(attfn,header=None)
                    attdat.columns=a1_states.columns
                    attdat.index=a1_states.index
                    ko_attrs = irr_gns[irr_gns.count(axis=1)>0].index
                    for attr_ind in ko_attrs:
                        a0 = attdat.loc[attr_ind].astype(int)
                        a1 = a1_states.loc[attr_ind].astype(int)
                        attractor_args_d[(oord,ss,rr,rep,attr_ind)] =  (a0.loc[binstates_df.columns],a1.loc[binstates_df.columns])
                        airr_gns = irr_gns.loc[attr_ind].fillna(0).astype(int)
                        arev_gns = rev_gns.loc[attr_ind].fillna(0).astype(int)
                        aunch_gns = ((airr_gns==0) & (arev_gns==0)).astype(int)
                        gene_status_d[(oord,ss,rr,rep,attr_ind,'irr')] = airr_gns
                        gene_status_d[(oord,ss,rr,rep,attr_ind,'rev')] = arev_gns
                        gene_status_d[(oord,ss,rr,rep,attr_ind,'unch')] = aunch_gns
        gene_status_df = pd.DataFrame(gene_status_d).T
        gene_status_df.to_pickle('results/crp/gene_status_df.pkl')
        with open('results/crp/attractor_args_d.pkl','wb') as fh:
            P.dump(attractor_args_d,fh,-1)
    else:
        attractor_args_d = pd.read_pickle('results/crp/attractor_args_d.pkl')
        gene_status_df = pd.read_pickle('results/crp/gene_status_df.pkl')
    
    for bpj,lod in bpj_tup_d.items():
        for jj,ofd in enumerate(lod):
            print(bpj,jj)
            on_mdrows = list(set(ofd['ON']) & set(mdrow2col_v.index))
            on_cols = mdrow2col_v.loc[on_mdrows]
            on_states = binstates_df.loc[on_cols]
            off_mdrows = list(set(ofd['OFF']) & set(mdrow2col_v.index))
            off_cols = mdrow2col_v.loc[off_mdrows]
            off_states = binstates_df.loc[off_cols]
            b0 = (on_states.mean()>gsym_bias_ser.loc[on_states.columns]).astype(int)
            b0 = b0.loc[binstates_df.columns]
            b1 = (off_states.mean()>gsym_bias_ser.loc[off_states.columns]).astype(int)
            b1 = b1.loc[binstates_df.columns]
            p_boltz = partial(calc_attr_weight_boltz,b0_b1=(b0,b1),act_probs=gsym_bias_ser.loc[b0.index])
            p_hamming = partial(calc_attr_weight_hamming,b0_b1=(b0,b1))
            ## calculate the distance between a1 and observed attractor
            boltz_op = list(futures.map(p_boltz,attractor_args_d.items()))
            hamming_op = list(futures.map(p_hamming,attractor_args_d.items()))
            lbl_l,hamm_l,wt_l = zip(*hamming_op)
            hamming_wts = pd.Series(dict(zip(lbl_l,wt_l)))
            hamming_dists = pd.Series(dict(zip(lbl_l,hamm_l)))
            boltz_wts = pd.Series(dict(boltz_op))
            ## need to sum all weights & normalize
            hamming_wts/=hamming_wts.sum()
            boltz_wts/=boltz_wts.sum()
            ## return weight & a triple (irrev, rev, unchanged) for each gene for each KO instance
            
            irr_boltz_avg = (gene_status_df.xs('irr',level=-1).T * boltz_wts).sum(axis=1)
            rev_boltz_avg = (gene_status_df.xs('rev',level=-1).T * boltz_wts).sum(axis=1)
            unch_boltz_avg = (gene_status_df.xs('unch',level=-1).T * boltz_wts).sum(axis=1)
            irr_hamming_avg = (gene_status_df.xs('irr',level=-1).T * hamming_wts).sum(axis=1)
            rev_hamming_avg = (gene_status_df.xs('rev',level=-1).T * hamming_wts).sum(axis=1)
            unch_hamming_avg = (gene_status_df.xs('unch',level=-1).T * hamming_wts).sum(axis=1)
            boltz_summaries[(bpj,jj,'irr')]=irr_boltz_avg
            boltz_summaries[(bpj,jj,'rev')]=rev_boltz_avg
            boltz_summaries[(bpj,jj,'unch')]=unch_boltz_avg
            hamming_summaries[(bpj,jj,'irr')]=irr_hamming_avg
            hamming_summaries[(bpj,jj,'rev')]=rev_hamming_avg
            hamming_summaries[(bpj,jj,'unch')]=unch_hamming_avg
            wts_summaries[(bpj,jj,'boltz')]=boltz_wts
            wts_summaries[(bpj,jj,'hamming')]=hamming_wts
    with open(f'results/crp/hamming_summaries{ext}.pkl','wb') as fh:
        P.dump(hamming_summaries,fh,-1)
    with open(f'results/crp/boltz_summaries{ext}.pkl','wb') as fh:
        P.dump(boltz_summaries,fh,-1)
    with open(f'results/crp/wts_summaries{ext}.pkl','wb') as fh:
        P.dump(wts_summaries,fh,-1)
    return

def identify_crp_metadata():
    metadata = pd.read_pickle('tmp/ecoli_metadata.pkl')
    all_logtpm_dat = pd.read_pickle('tmp/all_logtpm_dat.pkl')
    col2mdrow = {}
    for col in all_logtpm_dat.columns:
        if col in metadata.SRR_list.values:
            col2mdrow[col] = metadata[metadata.SRR_list==col].index[0]
        elif col in metadata.SRX.values:
            col2mdrow[col] = metadata[metadata.SRX==col].index[0]
        else:
            col2mdrow[col] = np.nan
    col2mdrow = pd.Series(col2mdrow)
    metadata = metadata[metadata.index.isin(col2mdrow[~col2mdrow.isna()])]
    crp_metadata = metadata[['crp' in gt if isinstance(gt,str) else False for gt in metadata.Genotype.values]]
    col2mdrow_v =  col2mdrow[~col2mdrow.isna()].astype(int)
    mdrow2col_v = pd.Series(dict(zip(col2mdrow_v.values,col2mdrow_v.index)))
    return mdrow2col_v
    
def obtain_main_inputs(mdrow2col_v,default_bias=True):
    all_logtpm_dat = pd.read_pickle('tmp/all_logtpm_dat.pkl')
    repgns = {'citB':'dpiA','srlM':'gutM','yahA':'pdeL'}
    all_logtpm_dat = all_logtpm_dat.T[all_logtpm_dat.count()>0].T
    all_logtpm_d = {}
    for (gsym,bno),row in all_logtpm_dat.iterrows():
        all_logtpm_d[(repgns.get(gsym,gsym),bno)] = row
    all_logtpm_dat = pd.DataFrame(all_logtpm_d).T
    rows_l = []
    for kk,vv in bpj_tup_d.items():
        for dd in vv:
            for kk2,vv2 in dd.items():
                rows_l.append(np.asarray(vv2,dtype=int))
    all_selected_rows = np.sort(np.hstack(rows_l))
    if isinstance(default_bias,bool):
        gsym_thr_ser = pd.read_pickle('tmp/gsym_thr_ser.pkl')
        gsym_bias_ser = pd.read_pickle('tmp/gsym_bias_ser.pkl')
    elif isinstance(default_bias,str):
        if default_bias=='zero':
            gsym_bias_ser = pd.read_pickle('tmp/gsym_biasz_ser.pkl')
            gsym_thr_d = {}
            for gsym,bz in gsym_bias_ser.items():
                gsym_thr_d[gsym]=bz
            gsym_thr_ser = pd.Series(gsym_thr_d)
        elif default_bias=='median':
            gsym_thr_ser = all_logtpm_dat.median(axis=1).droplevel(1)
            gsym_bias_d = {}
            for gsym,xthr in gsym_thr_ser.items():
                gsym_bias_d[gsym]=0.5
            gsym_bias_ser = pd.Series(gsym_bias_d)
        elif default_bias=='average':
            gsym_thr_ser = all_logtpm_dat.mean(axis=1).droplevel(1)
            gsym_bias_d = {}
            for gsym,xthr in gsym_thr_ser.items():
                gsym_bias_d[gsym]=(all_logtpm_dat.droplevel(1).loc[gsym,:]>xthr).mean()
            gsym_bias_ser = pd.Series(gsym_bias_d)
    gsym_thr_d = {}
    for kk,bb in gsym_thr_ser.items():
        gsym_thr_d[repgns.get(kk,kk)]=bb
    gsym_thr_ser = pd.Series(gsym_thr_d)    
    
    gsym_bias_d = {}
    for kk,bb in gsym_bias_ser.items():
        gsym_bias_d[repgns.get(kk,kk)]=bb
    gsym_bias_ser = pd.Series(gsym_bias_d)
    
    binstates_df = (all_logtpm_dat.droplevel(1).T>gsym_thr_ser.loc[all_logtpm_dat.index.get_level_values(0)]).astype(int)
    sel_binstates_df = binstates_df.loc[mdrow2col_v.loc[all_selected_rows]]
    return sel_binstates_df,gsym_bias_ser

if __name__=='__main__':
    ## could also attempt another binstates
    sb = True
    if len(sys.argv)>1:
        if sys.argv[1].startswith(('z','Z')):
            sb = 'zero'
        elif sys.argv[1].startswith(('m','M')):
            sb = 'median'
        elif sys.argv[1].startswith(('a','A')):
            sb = 'average'
    mdrow2col_v = identify_crp_metadata()
    binstates_df,gsym_bias_ser = obtain_main_inputs(mdrow2col_v,sb) 
    main(mdrow2col_v,binstates_df,gsym_bias_ser,sb)
