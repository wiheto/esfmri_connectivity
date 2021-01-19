import pandas as pd
from esfmri_connectivity.utils.getfiles import get_timeseries
import bct
import numpy as np
import matplotlib.pyplot as plt
import plotje

com_path = './esfmri_connectivity/communitydetection/data/'
bids_dir = '/home/william/sherlock/scratch/data/esfmri/'
save_dir = './esfmri_connectivity/analysis1/data/'

# Get parcel info at stimsite and only if that parcel is included for the subject
stim_df = pd.read_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t', index_col=0)
stim_df = stim_df[stim_df['parcel_included_in_sub_mask']==True]
stim_df = stim_df[stim_df['stimsite_issingleton']==0]


## Step 1, get the PC at the stim site for all runs (using concatentated es-fMRI to get the PC)

# Grab data for each subject/task and load
files, savelabels = get_timeseries(group='subtask', task='task-es')
pc = {}
for fi, filecol in enumerate(files):
    ts = []
    for f in filecol:
        ts.append(pd.read_csv(f, index_col=[0], sep='\t').transpose())
    sub = filecol[0].split('sub-')[1].split('_')[0]
    # Make pearson correlations over all runs for each subject/task
    ts = pd.concat(ts)
    ts.reset_index(inplace=True, drop=True)
    parcel_indices = ts.columns
    # Make connectivity matrices
    g = ts.corr().values
    g[g < 0] = 0
    # load communities
    com = pd.read_csv(com_path + 'sub-' + sub + '_task-es' + '_communities.tsv', sep='\t', index_col=[0])
    # calclate participation coefficent
    p = bct.participation_coef(g, com['communities'].values)
    for i, row in stim_df[stim_df['subject'] == int(sub)].iterrows():
        pc[i] = p[np.where(np.array(com.index)==int(row['overlapping_parcel_index']))[0]]

# add to stim_df dataframe
df_pc = pd.DataFrame(data={'PC': np.concatenate(list(pc.values()))}, index=pc.keys())
df_pc.sort_index(inplace=True)
stim_df['PC'] = df_pc['PC']

stim_df.to_csv('./esfmri_connectivity/analysis2/data/pc_at_stimsite.tsv', sep='\t')

# Plot figure (no colourdiff)
fig, ax = plt.subplots(1)
sublabs = []
color = ['gray', 'gray']
for subi, sub in enumerate(np.unique(stim_df['subject'])):
    sublabs.append(sub)
    subdf = stim_df[stim_df['subject'] == int(sub)]
    ci = np.remainder(subi, 2)
    ax.scatter(subdf['PC'], subi+np.zeros(len(subdf)),color=color[ci])

plotje.styler(ax, xlabel='PC', ylabel='Subjects', aspectsquare=True, title='PC of stimualtion site at different es runs')
ax.set_yticks(np.arange(0, len(sublabs)))
ax.set_yticklabels(sublabs)
ax.set_xticks(np.arange(0.2, 0.91, 0.1))
ax.set_xticklabels(np.round(np.arange(0.2, 0.91, 0.1),2))

#save
fig.savefig('./esfmri_connectivity/analysis2/figures/pc_at_stimsite.png', r=600)
fig.savefig('./esfmri_connectivity/analysis2/figures/pc_at_stimsite.svg')



# Plot figure (subcortical)
fig, ax = plt.subplots(1)
sublabs = []
color = ['lightgray', 'gray']
a = 0
b = 1
for subi, sub in enumerate(np.unique(stim_df['subject'])):
    sublabs.append(sub)
    subdf = stim_df[stim_df['subject'] == int(sub)]
    if len(subdf[subdf['overlapping_parcel_index']>400]) > 0: 
        tmp = subdf[subdf['overlapping_parcel_index']>400]
        if a == 0:
            lab = 'Subcortical'
            a = 1
        else:
            lab = None
        ax.scatter(tmp['PC'], subi+np.zeros(len(tmp)),color=color[0], label=lab)
    if len(subdf[subdf['overlapping_parcel_index']<=400]) > 0: 
        if a == 0:
            lab = 'Cortical'
            a = 1
        else:
            lab = None
        tmp = subdf[subdf['overlapping_parcel_index']<=400]
        ax.scatter(tmp['PC'], subi+np.zeros(len(tmp)),color=color[1], label=None)

plotje.styler(ax, xlabel='PC', ylabel='Subjects', aspectsquare=True, title='PC of stimualtion site at different es runs', legend=True)
ax.set_yticks(np.arange(0, len(sublabs)))
ax.set_yticklabels(sublabs)
ax.set_xticks(np.arange(0.2, 0.91, 0.1))
ax.set_xticklabels(np.round(np.arange(0.2, 0.91, 0.1),2))

#save
fig.savefig('./esfmri_connectivity/analysis2/figures/pc_at_stimsite_cortical.png', r=600)
fig.savefig('./esfmri_connectivity/analysis2/figures/pc_at_stimsite_cortical.svg')


