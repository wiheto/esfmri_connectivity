import pandas as pd
from esfmri_connectivity.utils.getfiles import get_timeseries, get_events
import bct
import bids

com_path = './esfmri_connectivity/communitydetection/data/'
bids_dir = '/data/'
save_dir = './esfmri_connectivity/analysis1/data/'

# Grab data for each subject/task and load
files = get_timeseries(task='task-es', require_stiminfo=True)
layout = bids.BIDSLayout(bids_dir)
for _, f in enumerate(files):
    print(f)
    savelabels = f.split('/')[-1].split('_space-')[0]
    sub = savelabels.split('_')[0].split('-')[1]
    run = f.split('run-')[1].split('_')[0]
    # Sub-314 only has events in run 01. Rest are the same (checked)
    if sub == '314': 
        r = '01'
    else:
        r = run
    eson, esoff = get_events(
    bids_dir, subject=sub, run=r, return_type=None, layout=layout)
    tstmp = pd.read_csv(f, index_col=[0], sep='\t')
    ts_eson = tstmp[eson.astype(str)].transpose()
    ts_esoff = tstmp[esoff.astype(str)].transpose()
    parcel_index = ts_eson.columns
    # Load communities
    com = pd.read_csv(com_path + 'sub-' + sub + '_task-es' + '_communities.tsv', sep='\t', index_col=[0])
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
            savelabels + '_desc-eson_connectivity.tsv', sep='\t')
    df = pd.DataFrame(g_esoff, columns=parcel_index, index=parcel_index)
    df.to_csv(save_dir + 'fc/' +
            savelabels + '_desc-esoff_connectivity.tsv', sep='\t')
    df = pd.DataFrame(data={'participation_coeff': part_eson,
                            'within_module_degree_zscore': z_eson}, index=parcel_index)
    df.to_csv(save_dir + 'cartprofile/' +
            savelabels + '_desc-eson_cartprofile.tsv', sep='\t')
    df = pd.DataFrame(data={'participation_coeff': part_esoff,
                            'within_module_degree_zscore': z_esoff}, index=parcel_index)
    df.to_csv(save_dir + 'cartprofile/' +
            savelabels + '_desc-esoff_cartprofile.tsv', sep='\t')




