"""
This script plots post hoc analysis 1, strength changes for all subjects
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotje
from matplotlib import cm

# Get parcel info at stimsite and only if that parcel is included for the subject
df = pd.read_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t', index_col=0)
df = df[df['parcel_included_in_sub_mask']==True]
community_path = './esfmri_connectivity/communitydetection/data/'

# load community information
communities = {}
labels = {}
for sub in np.unique(df['subject'].values):
    communities[sub] = pd.read_csv(community_path + '/sub-' + str(sub) + '_task-es_communities.tsv', index_col=[0], sep='\t')
    labels[sub] = pd.read_csv(community_path + '/sub-' + str(sub) + '_task-es_labels.tsv', index_col=[0], sep='\t')

med_all = {}
fig, ax = plt.subplots(11,4)
ax = ax.flatten()
dfs = df.copy()
dfs = df.sort_values(['subject', 'run'])


cols = {n: cm.Set2(i) for i, n in enumerate(np.unique(pd.concat(labels).values))}
template_conn_mat = {n: {m: [] for m in cols} for n in cols}

for axid, (i, row) in enumerate(dfs.iterrows()):
    fc_off = pd.read_csv('./esfmri_connectivity/analysis1/data/fc/sub-' + str(row['subject'])  + '_ses-postop_task-es_run-' + str(row['run']).zfill(2) + '_desc-esoff_connectivity.tsv', sep='\t', index_col=[0])
    fc_on = pd.read_csv('./esfmri_connectivity/analysis1/data/fc/sub-' + str(row['subject'])  + '_ses-postop_task-es_run-' + str(row['run']).zfill(2) + '_desc-eson_connectivity.tsv', sep='\t', index_col=[0])
    cs = communities[row['subject']]
    ls = labels[row['subject']]
    ssid = cs.loc[df[((df['subject']==row['subject']) & (df['run']==row['run']))]['overlapping_parcel_index']].values

    stim_label = ls.loc[ssid[0][0]].values[0]

    fc_diff = fc_on - fc_off

    coms_nonsing = [r for r in np.unique(cs.communities) if sum(cs['communities']==r) > 1]
    comstrdiff = np.zeros([len(coms_nonsing)])
    x = list(cs['communities'][cs['communities']==ssid[0][0]].index)
    fc_diff = fc_diff.loc[x]
    fc_diff = fc_diff.transpose()
    fc_diff.index = fc_diff.index.astype(int)
    key = 'sub: ' + str(row['subject']) + '\nrun: ' + str(row['run'])
    med_all[key] = []
    lss = []
    for cind1 in coms_nonsing:
        if cind1 != ssid:
            lss.append(str(ls.loc[cind1].values[0]))
            y = list(cs['communities'][cs['communities']==cind1].index)
            med_all[key].append(np.median(fc_diff.loc[y].values.flatten()))


    med_ind = np.argsort(med_all[key])[::-1]
    med_all[key] = np.sort(med_all[key])[::-1]

    ax[axid].plot([-1, len(med_all[key])], [0, 0], color='black')
    for x, k in enumerate(med_all[key]):
        ax[axid].bar(x, k, color=cols[lss[med_ind[x]]])
    ax[axid].scatter(-1, 0, color=cols[stim_label], zorder=100)
    ax[axid].set_ylim([-np.max(np.abs(med_all[key])), np.max(np.abs(med_all[key]))])
    plotje.styler(ax[axid], bottomaxis='off', leftaxis='off')
    ax[axid].text(len(med_all[key])-2, 0, key, fontsize=5)
fig.tight_layout()

fig.savefig('./esfmri_connectivity/analysis1/figures/str_diff_all.png', r=600)
fig.savefig('./esfmri_connectivity/analysis1/figures/str_diff_all.svg')

fig, ax = plt.subplots(1)
for i, c in enumerate(cols.keys()):
    ax.barh(i, 1, color=cols[c])

ax.set_yticks(np.arange(0, i+1))
ax.set_yticklabels(list(cols.keys()))
fig.tight_layout()


fig.savefig('./esfmri_connectivity/analysis1/figures/networkcolors.png', r=600)
fig.savefig('./esfmri_connectivity/analysis1/figures/networkcolors.svg')

