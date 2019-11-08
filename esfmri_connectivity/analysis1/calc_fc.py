import numpy as np
import pandas as pd
from esfmri_connectivity.utils.getfiles import get_timeseries, get_events
from plotje import styler
import matplotlib.pyplot as plt
import bct
com_path = './esfmri_connectivity/communitydetection/data/'
bids_dir = '/home/william/sherlock/scratch/data/esfmri/'
save_dir = './esfmri_connectivity/analysis1/data/'

# Grab data for each subject/task and load
files, savelabels = get_timeseries(group='subtask', task='task-es')
chosen_resolution = []
# Have to assume sub-314 runs are the same across all runs
for fi, filecol in enumerate(files):
    print(filecol)
    sub = savelabels[fi].split('_')[0].split('-')[1]
    ts_eson = []
    ts_esoff = []
    for f in filecol:
        run = f.split('run-')[1].split('_')[0]
        eson, esoff = get_events(
            bids_dir, subject=sub, run=run, return_type=None)
        tstmp = pd.read_csv(f, index_col=[0], sep='\t')
        ts_eson.append(tstmp[eson.astype(str)].transpose())
        ts_esoff.append(tstmp[esoff.astype(str)].transpose())

    ts_eson = pd.concat(ts_eson)
    ts_eson.reset_index(inplace=True, drop=True)
    ts_esoff = pd.concat(ts_esoff)
    ts_esoff.reset_index(inplace=True, drop=True)
    
    parcel_index = ts_eson.columns
    # Load communities
    com = pd.read_csv(com_path + savelabels[fi] + '_communities.tsv', sep='\t', index_col=[0])
    if any(com.index != parcel_index):
        raise ValueError('indices are different')
    # make connectivity matrices
    g_eson = ts_eson.corr().values
    g_esoff = ts_esoff.corr().values
    # Calc PC and z on eson
    gth_eson = g_eson.copy()
    gth_eson[gth_eson < 0] = 0
    part_eson = bct.participation_coef(gth_eson, com['communities'].values)
    z_eson = bct.module_degree_zscore(g_eson, com['communities'].values)
    # Calc PC and z on esoff
    gth_esoff = g_esoff.copy()
    gth_esoff[gth_esoff < 0] = 0
    part_esoff = bct.participation_coef(gth_esoff, com['communities'].values)
    z_esoff = bct.module_degree_zscore(g_esoff, com['communities'].values)
    # Save all the files as tsvs
    df = pd.DataFrame(g_eson, columns=parcel_index, index=parcel_index)
    df.to_csv(save_dir + 'fc/' +
              savelabels[fi] + '_desc-eson_connectivity.tsv', sep='\t')
    df = pd.DataFrame(g_esoff, columns=parcel_index, index=parcel_index)
    df.to_csv(save_dir + 'fc/' +
              savelabels[fi] + '_desc-esoff_connectivity.tsv', sep='\t')
    df = pd.DataFrame(data={'participation_coeff': part_eson,
                            'within_module_degree_zscore': z_eson}, index=parcel_index)
    df.to_csv(save_dir + 'cartprofile/' +
              savelabels[fi] + '_desc-eson_cartprofile.tsv', sep='\t')
    df = pd.DataFrame(data={'participation_coeff': part_esoff,
                            'within_module_degree_zscore': z_esoff}, index=parcel_index)
    df.to_csv(save_dir + 'cartprofile/' +
              savelabels[fi] + '_desc-esoff_cartprofile.tsv', sep='\t')