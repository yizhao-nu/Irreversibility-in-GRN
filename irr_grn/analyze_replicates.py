
"""
analyze_replicates.py
Resample different network reconstructions to determine whether the averages agree.
Reproduces Fig. S1 of the paper.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype']='none'
from glob import glob
import os.path as osp
from collections import defaultdict
from itertools import combinations as combs
from scipy.stats import gmean,scoreatpercentile as SAP
from scipy.special import comb
import pickle as P
import time

def analyze_replicates(df_d,selg,MAX_SAMP=1e3):
    nn_keyval_l = []
    mm_keyval_l = []
    ELT0 = list(df_d.values())[0]
    L = ELT0.shape[1]
    tS = set([])
    for igns in df_d['ovr'].values:
        tS |= set(igns)
    for nn in range(1,int(L/2)+1):
        print(nn)
        output_dd = defaultdict(list)
        gn_pctdiff = defaultdict(list)
        NCMB = comb(ELT0.columns.shape[0],nn)
        MCMB = int(comb(ELT0.columns.shape[0]-nn,nn))
        TOT_CMB = NCMB*MCMB
        if TOT_CMB > MAX_SAMP:
            rng = np.random.default_rng()
            NPC = int(MAX_SAMP/NCMB)+1
            ctr=0
        for ncmb in combs(ELT0.columns,nn):
            if TOT_CMB > MAX_SAMP:
                num_gen = [elt for zzz,elt in enumerate(rng.permutation(MCMB)) if zzz<NPC]
            unsel = set(ELT0.columns)-set(ncmb)
            nmu_d = dict([(kw,df.loc[selg,ncmb].mean(axis=1)) 
                          if isinstance(df,pd.DataFrame) 
                          else (kw,gmean(df.loc[list(ncmb)])) 
                          for kw,df in df_d.items() if kw !='ovr'])
            nS = set([])
            for igns in df_d['ovr'].loc[list(ncmb)]:
                nS |= set(igns)
            for mmm,mcmb in enumerate(combs(unsel,nn)):
                if TOT_CMB > MAX_SAMP:
                    if mmm not in num_gen:
                        continue
                    if ctr > MAX_SAMP-1:
                        break
                    else: #uncomment these lines to sample
                        ctr+=1
                for kw,df in df_d.items():
                    if isinstance(df,pd.DataFrame):
                        cmp = df.loc[selg,mcmb].mean(axis=1)
                        NUMER = (nmu_d[kw]-cmp)
                        DENOM = (nmu_d[kw]+cmp)
                        for (SRT,SS,RR,gn),denom in DENOM.items():
                            ## Note the unpacking of additional parameters: (SRT,SS,RR,gn)
                            if np.abs(denom)>1e-9:
                                gn_pctdiff[(kw,gn)].append(2*np.abs(NUMER.loc[(SRT,SS,RR,gn)])/denom)
                            elif np.abs(denom)<1e-9 and np.abs(NUMER.loc[(SRT,SS,RR,gn)])<1e-9:
                                gn_pctdiff[(kw,gn)].append(0)
                            elif np.abs(denom)<1e-9:
                                gn_pctdiff[(kw,gn)].append(np.nan)
                        output_dd[(kw,'rmsd')].append(np.sqrt(np.mean(np.square(NUMER))))
                        output_dd[(kw,'max')].append(np.amax(np.abs(NUMER)))
                    else:
                        if kw=='ovr':
                            mS = set([])
                            for igns in df_d['ovr'].loc[list(mcmb)]:
                                mS |= set(igns)
                            ## jaccard difference between two sets
                            output_dd[(kw,'max')].append(len(mS&nS)/len(mS|nS))
                            ## overall recovery of the total ...?
                            output_dd[(kw,'rmsd')].append(len(mS&nS)/len(tS)) 
                        else:
                            cmp = gmean(df.loc[list(mcmb)])
                            output_dd[(kw,'rmsd')].append(np.abs(nmu_d[kw]-cmp))
        ## need to postprocess the output
        output_d = dict(output_dd)
        for kk,vv in output_d.items():
            if kk=='ovr':
                VV = pd.Series(vv,dtype='float64').value_counts()
                nn_keyval_l.append(((nn,kk[0],kk[1]),VV))
            else:
                VV = pd.Series(vv,dtype='float64').describe(percentiles=[0.025,.25,.50,.75,.975])
                nn_keyval_l.append(((nn,kk[0],kk[1]),VV))
        gn_pctdiff_d = dict(gn_pctdiff)
        for kk,vv in gn_pctdiff_d.items():
            VV = pd.Series(vv,dtype='float64').describe(percentiles=[0.025,.25,.50,.75,.975])
            mm_keyval_l.append(((nn,kk[0],kk[1]),VV))
    return nn_keyval_l,mm_keyval_l

def analyze_irr_sets(irrev,MAX_SAMP=1e3):
    isIrrev = irrev>0
    irr_gns = irrev[(isIrrev).any(axis=1)].index.get_level_values(-1)
    nn_l = []
    for nn in range(int(irrev.shape[1])):
        print(nn)
        if nn<1:
            continue
        ovr_l = []
        NCMB = comb(irrev.columns.shape[0],nn)
        if NCMB > MAX_SAMP:
            rng = np.random.default_rng()
            num_gen = [elt for zzz,elt in enumerate(rng.permutation(int(NCMB))) if zzz<MAX_SAMP]
            ctr = 0
        for mmm,ncmb in enumerate(combs(irrev.columns,nn)):
            if NCMB > MAX_SAMP:
                if mmm not in num_gen:
                    continue
                if ctr > MAX_SAMP-1:
                    break
                else: #uncomment these lines to sample
                    ctr+=1            
            cmb_irr_gns = irrev[isIrrev.loc[:,ncmb].any(axis=1)].index.get_level_values(-1)
            ovr = len(set(irr_gns) & set(cmb_irr_gns))
            ovr_l.append(ovr/len(irr_gns))
        nn_l.append(pd.Series(ovr_l,dtype='float64').value_counts())
    return nn_l

def output_results_by_rep(rep_params,state_df,irrev_df,numattr_ser):
    srt,ss,rr = rep_params
    selg = irrev_df.mean(axis=1).sort_values(ascending=False).index
    fig,ax_l = plt.subplots(2,1,figsize=(6.4,4.8))
    img = ax_l[0].imshow(irrev_df.loc[selg].sort_index(axis=1).T,norm='log',vmin=1e-3,vmax=1)
    cb1 = fig.colorbar(img, ax=ax_l[0],orientation='horizontal',location='top')
    cb1.set_label('Irreversibility',size=8)
    plt.setp(cb1.ax.xaxis.get_ticklabels(),size=6)
    ax_l[0].set_yticks(np.arange(irrev_df.shape[1]))
    ax_l[0].set_yticklabels(['%d' % ii for ii in numattr_ser.sort_index().values],size=6)
    ax_l[0].set_ylabel('Rep',size=8)
    ax_l[0].set_xticks(np.arange(51))
    ax_l[0].set_xticklabels(['' for ii in np.arange(51)],size=6,rotation=90, horizontalalignment='center')
    img2 = ax_l[1].imshow(state_df.loc[selg].sort_index(axis=1).T)
    cb2 = fig.colorbar(img2,ax=ax_l[1],orientation='horizontal',location='top')
    cb2.set_label('"On" probability',size=8)
    plt.setp(cb2.ax.xaxis.get_ticklabels(),size=6)
    ax_l[1].set_yticks(np.arange(state_df.shape[1]))
    ax_l[1].set_yticklabels(['%d' % ii for ii in numattr_ser.sort_index().values],size=6)
    ax_l[1].set_xticks(np.arange(51))
    ax_l[1].set_xticklabels(irrev_df.index.get_level_values(0),size=6,rotation=90, horizontalalignment='center')
    ax_l[1].set_ylabel('Rep',size=8)
    fig.suptitle('Parameters: %s   s=%s   r=%s' % (srt,ss,rr),size=10)
    plt.tight_layout()
    fig.savefig('figs/%s_%s_%s.png' % (srt,ss,rr))
    return

def main():
    with open('netfiles/twoparam_0.00_0.20_asc_00_0.bnet','r') as fh:
        asc_l = [ln.split(',')[0] for ln in fh]
    with open('netfiles/twoparam_0.00_0.20_desc_00_0.bnet','r') as fh:
        desc_l = [ln.split(',')[0] for ln in fh]
    if not osp.exists('tmp/irrev_ser.pkl'):
        irrev_d = {}
        avgstate_d = {}
        numattr_d = {}
        for aa,pt in enumerate(['KO','OE']):
            for bb,srt in enumerate(['desc','asc']):
                print(pt,srt)
                fn_l = glob("results/result-attr-trans-%s-twoparam_*_*_%s_*.csv" % (pt,srt))
                for fn in fn_l:
                    __,ss,rr,__,rep,__ = fn.split('/')[-1].split('_')
                    att_fn = "attfiles/1st_twoparam_%s_%s_%s_%s_%d.csv" % (ss,rr,srt,rep,int(rep))
                    if not osp.exists(att_fn):
                        print('missing',att_fn)
                        continue
                    attractors_df = pd.read_csv(att_fn,header=None)
                    if srt == 'asc':
                        attractors_df.columns = asc_l
                    else:
                        attractors_df.columns = desc_l
                    attractors_df.index = [elt for elt in range(1,attractors_df.shape[0]+1)]
                    results = pd.read_csv(fn,index_col=0)
                    vcs = results.pert_gene_name.value_counts()
                    if pt=='KO':
                        totals = (attractors_df.loc[:,vcs.index]>0).sum(axis=0)
                    elif pt=='OE':
                        totals = (attractors_df.loc[:,vcs.index]<1).sum(axis=0)
                    irrev_avgs = vcs/totals
                    for gn,avg_irrev in irrev_avgs.items():
                        ## the mean is taken across attractors
                        irrev_d[(srt,pt,ss,rr,rep,gn)] = avg_irrev 
                    if pt=='KO': ## this does not depend on the perturbation type
                        for gn,avgON in attractors_df.mean(axis=0).items():
                            avgstate_d[(srt,ss,rr,rep,gn)] = avgON
                        numattr_d[(srt,ss,rr,rep)] = attractors_df.shape[0]
        ## convert into series
        irrev_ser = pd.Series(irrev_d)
        irrev_ser.to_pickle('tmp/irrev_ser.pkl')
        avgstate_ser = pd.Series(avgstate_d)
        avgstate_ser.to_pickle('tmp/avgstate_ser.pkl')
        numattr_ser = pd.Series(numattr_d)
        numattr_ser.to_pickle('tmp/numattr_ser.pkl')
    else:
        irrev_ser = pd.read_pickle('tmp/irrev_ser.pkl')
        all_genes = irrev_ser.index.get_level_values(-1).unique()
        avgstate_ser = pd.read_pickle('tmp/avgstate_ser.pkl')
        numattr_ser = pd.read_pickle('tmp/numattr_ser.pkl')
        
    if osp.exists('tmp/overall_output_d.pkl'):
        overall_output_d = pd.read_pickle('tmp/overall_output_d.pkl')
    else:
        overall_output_d={}
    if osp.exists('tmp/overall_setovr_d.pkl'):
        overall_setovr_d = pd.read_pickle('tmp/overall_setovr_d.pkl')
    else:
        overall_setovr_d={}
    if osp.exists('tmp/overall_gnoutput_d.pkl'):
        overall_gnoutput_d = pd.read_pickle('tmp/overall_gnoutput_d.pkl')
    else:
        overall_gnoutput_d={}
    
    completed_params = []
    S1 = set([(kk[0],kk[1],kk[2]) for kk in overall_output_d.keys()])
    S2 = set([(kk[0],kk[1],kk[2]) for kk in overall_setovr_d.keys()])
    S3 = set([(kk[0],kk[1],kk[2]) for kk in overall_gnoutput_d.keys()])
    completed_params = S1&S2&S3
    avgstate_GB = avgstate_ser.groupby(level=[0,1,2])
    for rep_params,reps_grp in irrev_ser.groupby(level=[0,2,3]):
        rep_irrev_d = {}
        rep_nz_d = {}
        if rep_params in [('asc','0.00','1.00'),('asc','1.00','0.00')]:
            continue
        elif rep_params in completed_params:
            continue
        pert_gn_rep_irrev = reps_grp.unstack(-2).fillna(0)
        pert_gn_rep_irrev.index = pert_gn_rep_irrev.index.droplevel([0,2,3])
        state_df = avgstate_GB.get_group(rep_params).unstack(-2)
        for gn, rows in pert_gn_rep_irrev.groupby(level=-1):
            vvv = state_df.loc[tuple(list(rep_params)+[gn])]
            if rows.shape[0]==2:
                irr_avg_ovr_perts = (rows.loc[('KO',gn),:]*vvv + rows.loc[('OE',gn),:]*(1-vvv))
            elif rows.shape[0]==1 and 'KO' in rows.index.get_level_values(0):
                irr_avg_ovr_perts = rows.loc[('KO',gn),:]*vvv
            elif rows.shape[0]==1:
                irr_avg_ovr_perts = rows.loc[('OE',gn),:]*(1-vvv)
            else:
                irr_avg_ovr_perts = 0
            for rep,val in irr_avg_ovr_perts.items():
                kw = tuple(list(rep_params)+[gn,rep])
                rep_irrev_d[kw]=val
        irrev_df = pd.Series(rep_irrev_d).unstack(-1)
        for XGN in set(all_genes)-set(irrev_df.index.get_level_values(-1)):
            kw = tuple(list(rep_params)+[XGN])
            irrev_df.loc[kw] = pd.Series(np.zeros(irrev_df.shape[1]), index=irrev_df.columns)
        selg = irrev_df.mean(axis=1).sort_values(ascending=False).index
        for rep,col in irrev_df.items():
            rep_nz_d[rep]=col[col>0].index.get_level_values(-1).unique().tolist()
        nz_ser = pd.Series(rep_nz_d)
        numattr_rep_ser = numattr_ser.unstack(-1).loc[rep_params]
        #output_results_by_rep(rep_params,selg,state_df,irrev_df,numattr_rep_ser)
        ttt = time.time()
        summary_l,gnsummary_l = analyze_replicates({'irrev':irrev_df, 'state':state_df.loc[irrev_df.index], 'N_A':numattr_rep_ser,'ovr':nz_ser},selg)
        for elt in gnsummary_l:
            kk,vv = elt
            KW = tuple(list(rep_params)+list(kk[:3]))
            overall_gnoutput_d[KW]=vv
        for elt in summary_l:
            kk,vv = elt
            KW = tuple(list(rep_params)+list(kk[:3]))
            overall_output_d[KW]=vv
        with open('tmp/overall_output_d.pkl','wb') as fh:
            P.dump(overall_output_d,fh,-1)
        with open('tmp/overall_gnoutput_d.pkl','wb') as fh:
            P.dump(overall_gnoutput_d,fh,-1)
        ttt2 = time.time()
        print('analyze_replicates Elapsed: %.2f' % (ttt2-ttt))
        nn_l = analyze_irr_sets(irrev_df)
        ttt3 = time.time()
        for ii,vv in enumerate(nn_l):
            KW = tuple(list(rep_params)+[ii])
            overall_setovr_d[KW]=vv
        with open('tmp/overall_setovr_d.pkl','wb') as fh:
            P.dump(overall_setovr_d,fh,-1)
        print('analyze_irr_sets Elapsed: %.2f' % (ttt3-ttt2))
        print(rep_params)

if __name__ == '__main__':
    main()
