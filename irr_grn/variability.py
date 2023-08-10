# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 10:09:01 2022

@author: Yi Zhao
@author2: Thomas Wytock
"""
import pandas as pd
import networkx as nx
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy import optimize
from sklearn.metrics import r2_score
from sklearn.model_selection import LeaveOneOut as LOO
from collections import defaultdict
plt.rcParams['svg.fonttype']='none'

def main(nrep=10):
    loo = LOO()
    all_mean = []
    exps = [0,0.2,0.4,0.6,0.8,1.0]
    df_r2 = pd.DataFrame(index = exps[:-1])
    ## define the training and test set
    ## these are defined by the index of their replicate 
    ## (an integer between 0 and n_replicates=10, represented as a string)
    params_d = defaultdict(dict)
    params_l = ['r2','slope','intercept']
    #diffs_l = []; 
    loo_diffs = []
    for tr_inds,te_inds in loo.split(range(10)):
        tr_inds = ['%d' % a for a in tr_inds]
        te_inds = ['%d' % a for a in te_inds]        
        if te_inds[0]=='0':
            mus_l = []
        tr_means = []
        te_means = []
        for aa,pt in enumerate(['KO','OE']):
            for bb,srt in enumerate(['inv','so']):
                ## load the irreversibility probability
                results = pd.read_csv("results/df_neg2_pre_noNA_%s_%s.csv" % (pt,srt),index_col=0)
                ## load the state (oe/kd) frequencies
                states = pd.read_csv("results/states_neg2_pre_%s_%s.csv" % (pt,srt),index_col=0)
                ## split the index '<R parameter>-<replicate>' into a multi index using the '-' token as a delimiter
                ## The MultiIndex allows us to easily take a statistics over a fixed value of the R parameter.
                results.index = pd.MultiIndex.from_tuples([e.split('-') for e in results.index])
                states.index = pd.MultiIndex.from_tuples([e.split('-') for e in states.index])
                ## select the "training" and "test" halves of the data.
                res_tr = results[results.index.get_level_values(1).isin(tr_inds)]
                st_tr = states[states.index.get_level_values(1).isin(tr_inds)]
                res_te = results[results.index.get_level_values(1).isin(te_inds)]
                st_te = states[states.index.get_level_values(1).isin(te_inds)]
                ## With the multiindex and groupby functionality, 
                ## we can condense the "weighted_mean" functions into a single line
                wmu_tr = (res_tr*st_tr).groupby(level=0).sum()/st_tr.groupby(level=0).sum()
                wmu_te = (res_te*st_te).groupby(level=0).sum()/st_te.groupby(level=0).sum()
                tr_means.append(wmu_tr.mean(axis=0).fillna(0))
                te_means.append(wmu_te.mean(axis=0).fillna(0))
                if te_inds[0]=='0':
                    mus_l.append(((results*states).groupby(level=0).sum()/states.groupby(level=0).sum()).mean(axis=0))
        tr_means2 = pd.concat(tr_means,axis=1).mean(axis=1)
        te_means2 = pd.concat(te_means,axis=1).mean(axis=1)
        loo_diffs.append(te_means2-tr_means2)
        if te_inds[0]=='0':
            ovr_avg = pd.concat(mus_l,axis=1).mean(axis=1).sort_values(ascending=False)
    aaa = pd.concat(loo_diffs,axis=1)
    bias = aaa.mean(axis=1)
    sig = aaa.std(axis=1)
    xvals = np.arange(ovr_avg.shape[0])
    fig = plt.figure(figsize=(7.5,2.5))
    ax = fig.add_axes([.08,0.23,0.91,0.73])
    ax.bar(xvals,ovr_avg,color='C0',alpha=0.7)
    ax.errorbar(xvals,ovr_avg+bias.loc[ovr_avg.index],yerr=1.96*sig.loc[ovr_avg.index]/np.sqrt(10),fmt='k.')
    ax.set_ylabel('Irreversibility probability')
    ax.set_xticks(xvals)
    ax.set_xlim(-1,xvals[-1]+1)
    ax.set_ylim(0,0.81)
    ax.set_xticklabels(ovr_avg.index,size=6.5,horizontalalignment='center',rotation=90)
    ax.set_xlabel('Gene')
    fig.savefig('probability_variability.svg')
    print('Done')

if __name__ == '__main__':
    main()
    