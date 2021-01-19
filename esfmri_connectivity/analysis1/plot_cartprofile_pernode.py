import matplotlib.pyplot as plt
import plotje
import pandas as pd
import numpy as np
import nibabel as nib
from nilearn import plotting
from matplotlib import cm

# Get parcel info at stimsite and only if that parcel is included for the subject
df = pd.read_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t', index_col=0)
df = df[df['parcel_included_in_sub_mask']==True]

cart_profile_path = './esfmri_connectivity/analysis1/data/cartprofile/'
community_path = './esfmri_connectivity/communitydetection/data/'

# load community information
communities = {}
labels = {}
for sub in np.unique(df['subject'].values):
    communities[sub] = pd.read_csv(community_path + '/sub-' + str(sub) + '_task-es_communities.tsv', index_col=[0], sep='\t')
    labels[sub] = pd.read_csv(community_path + '/sub-' + str(sub) + '_task-es_labels.tsv', index_col=[0], sep='\t', header=None)

# load the PC and z for each run
cartprofile_eson = {}
cartprofile_esoff = {}
for i, row in df.iterrows():
    fname = 'sub-' + str(row['subject']) + '_ses-postop_task-es_run-' + str(row['run']).zfill(2) + '_desc-eson_cartprofile.tsv'
    cartprofile_eson[i] = pd.read_csv(cart_profile_path + fname, sep='\t', index_col=[0])
    fname = 'sub-' + str(row['subject']) + '_ses-postop_task-es_run-' + str(row['run']).zfill(2) + '_desc-esoff_cartprofile.tsv'
    cartprofile_esoff[i] = pd.read_csv(cart_profile_path + fname, sep='\t', index_col=[0])

np.random.seed(2020)
randsub = np.random.permutation(list(cartprofile_eson.keys()))[0]

c = communities[df.loc[randsub]['subject']]
l = labels[df.loc[randsub]['subject']]
sid = c.loc[df.loc[randsub]['overlapping_parcel_index']].values
within_community = list(c[c==sid].dropna().index)
outside_community = list(c[c!=sid].dropna().index)
cp_on = cartprofile_eson[randsub]
cp_off = cartprofile_esoff[randsub]


fig, ax = plt.subplots(1, 2, figsize=(12,8))

ax[0].scatter(cp_on['participation_coeff'].loc[within_community].median(), cp_on['within_module_degree_zscore'].loc[within_community].median(), c='salmon', alpha=0.8, marker='s', s=100, zorder=100)
ax[0].scatter(cp_off['participation_coeff'].loc[within_community].median(), cp_off['within_module_degree_zscore'].loc[within_community].median(), c='cornflowerblue', alpha=0.8, marker='s', s=100, zorder=100)

for i, r in cp_on.loc[within_community].iterrows():
    ax[0].plot([r['participation_coeff'], cp_off.loc[i]['participation_coeff']], [r['within_module_degree_zscore'], cp_off.loc[i]['within_module_degree_zscore']], color='gray', alpha=0.2)

ax[0].scatter(cp_on['participation_coeff'].loc[within_community], cp_on['within_module_degree_zscore'].loc[within_community], c='salmon', alpha=0.4, label='es on')
ax[0].scatter(cp_off['participation_coeff'].loc[within_community], cp_off['within_module_degree_zscore'].loc[within_community], c='cornflowerblue', alpha=0.4, label='es off')

ax[0].scatter(-100,100, c='gray', alpha=0.4, label='node', marker='o')
ax[0].scatter(-100,100, c='gray', alpha=0.4, label='median', marker='s')


ax[1].scatter(cp_on['participation_coeff'].loc[outside_community].median(), cp_on['within_module_degree_zscore'].loc[outside_community].median(), c='salmon', alpha=0.8, marker='s', s=100, zorder=100)
ax[1].scatter(cp_off['participation_coeff'].loc[outside_community].median(), cp_off['within_module_degree_zscore'].loc[outside_community].median(), c='cornflowerblue', alpha=0.8, marker='s', s=100, zorder=100)

for i, r in cp_on.loc[outside_community].iterrows():
    ax[1].plot([r['participation_coeff'], cp_off.loc[i]['participation_coeff']], [r['within_module_degree_zscore'], cp_off.loc[i]['within_module_degree_zscore']], color='gray', alpha=0.2)

ax[1].scatter(cp_on['participation_coeff'].loc[outside_community], cp_on['within_module_degree_zscore'].loc[outside_community], c='salmon', alpha=0.4, label='es on')
ax[1].scatter(cp_off['participation_coeff'].loc[outside_community], cp_off['within_module_degree_zscore'].loc[outside_community], c='cornflowerblue', alpha=0.4, label='es off')


for a in ax:
    a.set_xlim([0.4, 1])
    a.set_ylim([-3.6, 2.5])

plotje.styler(ax[0], title='Within stimulation community', aspectsquare=True, legend=True, xlabel='Participation coefficient', ylabel='Within module degree z-score')
plotje.styler(ax[1], title='Outside stimulation community', aspectsquare=True, legend=False, xlabel='Participation coefficient', ylabel='Within module degree z-score')

for a in ax:
    a.set_xticks([0.5, 0.7, 0.9])
    a.set_yticks([-2, 0, 2])
    a.set_xticklabels([0.5, 0.7, 0.9])
    a.set_yticklabels([-2, 0, 2])

fig.tight_layout()

fig.savefig('./esfmri_connectivity/analysis1/figures/cartprofile_pernode_examplesubject.svg')
fig.savefig('./esfmri_connectivity/analysis1/figures/cartprofile_pernode_examplesubject.png', r=600)


sub = str(df.loc[randsub]['subject'])
run = str(df.loc[randsub]['run'])
print('random subject was: ' + sub + ', run ' + run)


a= 0
fig, ax = plt.subplots(2, 4)
ax = ax.flatten()

ax[0].scatter(cp_on['participation_coeff'].loc[within_community].median(), cp_on['within_module_degree_zscore'].loc[within_community].median(), c='salmon', alpha=0.8, marker='s', s=5, edgecolor='black', linewidth=0.3, zorder=100)
ax[0].scatter(cp_off['participation_coeff'].loc[within_community].median(), cp_off['within_module_degree_zscore'].loc[within_community].median(), c='cornflowerblue', alpha=0.8, marker='s', s=5, edgecolor='black', linewidth=0.3, zorder=100)

for i, r in cp_on.loc[within_community].iterrows():
    ax[0].plot([r['participation_coeff'], cp_off.loc[i]['participation_coeff']], [r['within_module_degree_zscore'], cp_off.loc[i]['within_module_degree_zscore']], color='gray', alpha=0.2)

ax[0].scatter(cp_on['participation_coeff'].loc[within_community], cp_on['within_module_degree_zscore'].loc[within_community], c='salmon', alpha=0.4, label='es on', s=3)
ax[0].scatter(cp_off['participation_coeff'].loc[within_community], cp_off['within_module_degree_zscore'].loc[within_community], c='cornflowerblue', alpha=0.4, label='es off', s=3)


for i, cid in enumerate(np.unique(c['communities'])): 
    if np.sum(c['communities'] == cid) > 10 and cid != sid:
        a+=1
        incom = list(c[c==cid].dropna().index)
        ax[a].scatter(cp_on['participation_coeff'].loc[incom].median(), cp_on['within_module_degree_zscore'].loc[incom].median(), c='salmon', alpha=0.8, marker='s', s=5, edgecolor='black', linewidth=0.3, zorder=100)
        ax[a].scatter(cp_off['participation_coeff'].loc[incom].median(), cp_off['within_module_degree_zscore'].loc[incom].median(), c='cornflowerblue', alpha=0.8, marker='s', s=5, edgecolor='black', linewidth=0.3, zorder=100)

        for i, r in cp_on.loc[incom].iterrows():
            ax[a].plot([r['participation_coeff'], cp_off.loc[i]['participation_coeff']], [r['within_module_degree_zscore'], cp_off.loc[i]['within_module_degree_zscore']], color='gray', alpha=0.2)

        ax[a].scatter(cp_on['participation_coeff'].loc[incom], cp_on['within_module_degree_zscore'].loc[incom], c='salmon', alpha=0.4, label='es on', s=3)
        ax[a].scatter(cp_off['participation_coeff'].loc[incom], cp_off['within_module_degree_zscore'].loc[incom], c='cornflowerblue', alpha=0.4, label='es off', s=3)
    

ax[-1].scatter(-100,100, c='gray', alpha=0.4, label='node', marker='o', s=3)
ax[-1].scatter(-100,100, c='gray', alpha=0.4, label='median', marker='s', s=3)

for a in ax:
    a.set_xlim([0.4, 1])
    a.set_ylim([-3.6, 2.5])
    plotje.styler(a, aspectsquare=True, legend=False)

plotje.styler(ax[-1], aspectsquare=True, legend=True)


for a in ax:
    a.set_xticks([0.5, 0.7, 0.9])
    a.set_yticks([-2, 0, 2])
    a.set_xticklabels([0.5, 0.7, 0.9])
    a.set_yticklabels([-2, 0, 2])


fig.savefig('./esfmri_connectivity/analysis1/figures/cartprofile_pernode_examplesubject_outsidesplit.svg')
fig.savefig('./esfmri_connectivity/analysis1/figures/cartprofile_pernode_examplesubject_outsidesplit.png', r=600)

