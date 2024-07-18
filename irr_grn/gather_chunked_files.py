from glob import glob
import pandas as pd
import numpy as np
import os.path as osp
import os
def main():
    fps=['twoparam_0.00_0.40_asc_02_2', 'twoparam_0.00_0.40_asc_10_10', 'twoparam_0.20_0.80_asc_09_9', 
        'twoparam_0.20_0.80_asc_17_17', 'twoparam_0.20_1.00_asc_08_8', 'twoparam_0.40_0.60_asc_00_0', 
        'twoparam_0.40_0.60_asc_08_8', 'twoparam_0.40_0.60_asc_14_14', 'twoparam_0.40_0.60_asc_19_19', 
        'twoparam_0.40_1.00_asc_00_0', 'twoparam_0.40_1.00_asc_02_2', 'twoparam_0.40_1.00_asc_03_3', 
        'twoparam_0.40_1.00_asc_05_5', 'twoparam_0.40_1.00_asc_08_8', 'twoparam_0.40_1.00_asc_09_9', 
        'twoparam_0.40_1.00_asc_10_10', 'twoparam_0.40_1.00_asc_11_11', 'twoparam_0.40_1.00_asc_17_17', 
        'twoparam_0.80_1.00_asc_07_7', 'twoparam_0.80_1.00_asc_01_1', 'twoparam_0.60_1.00_asc_16_16', 
        'twoparam_0.40_1.00_asc_18_18']


    prefix_l = ['changed','result-OE','result-KO']
    Ntot = 48 ## this number must match the number of chunks, see the logging file names
    for fp in fps:
        for prefix in prefix_l:
            fns2comb_l = []
            dfs2comb_l = []
            for ii in range(1,Ntot+1):
                fn = f'results/{prefix}-{fp}-chunk-{ii}-of-{Ntot}.csv'
                if not osp.exists(fn):
                    break
                chunkres = pd.read_csv(fn,index_col=0)
                drop_rows = -1 if prefix=='changed' else -2
                chunkres = chunkres.iloc[:drop_rows]
                newinds = (np.asarray(chunkres.index.tolist())-1)*Ntot+ii
                chunkres.index=newinds
                dfs2comb_l.append(chunkres)
                fns2comb_l.append(fn)
            else:
                combined_df = pd.concat(dfs2comb_l,axis=0).sort_index()
                if prefix=='changed':
                    opfn = f'results/{prefix}-pre-{fp}.csv'
                    df2add = pd.DataFrame({combined_df.shape[0]+1:combined_df.mean(axis=0)}).T
                    combined_df = pd.concat([combined_df,df2add],axis=0)
                else:
                    opfn = f'results/{prefix}-{fp}-pre.csv'
                    colmeans = combined_df.mean(axis=0)
                    colsums = combined_df.sum(axis=0)
                    df2add = pd.DataFrame({(combined_df.shape[0]+1):colmeans,
                               (combined_df.shape[0]+2):colsums}).T
                    combined_df = pd.concat([combined_df,df2add],axis=0)
                combined_df.to_csv(opfn)
                ___ = [os.remove(fn) for fn in fns2comb_l]

if __name__=='__main__':
    main()
