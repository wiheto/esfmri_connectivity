import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotje
import seaborn as sns


def shufflegroups(dat1, dat2, pnum=10000, tail=1):
    """Dat1, dat2 are of equal length.
    Groups get shuffled pnum number of times with permuted groups equalling the len of
    inpput data. Shuffling ensures that data from the matched data end up in different permuted groups.
    i.e. dat1(x) and dat2(x) end up in opposite permuted groups
    Returns permutation distirbution of avg(perm(len(dat1))-avg(perm(len(dat2)).
    Funciton modified taken from teneto.
    """
    if len(dat1) != len(dat2):
        raise ValueError("dat vectors must be of same length")
    permdist = np.zeros(pnum)
    for i in range(0, pnum):
        porder = np.random.randint(1, 3, len(dat1))
        permutation_group1 = np.concatenate(
            (dat1[np.where(porder == 1)], dat2[np.where(porder == 2)]))
        permutation_group2 = np.concatenate(
            (dat1[np.where(porder == 2)], dat2[np.where(porder == 1)]))
        if tail == 2:
            permdist[i] = abs(np.nanmean(permutation_group1) - np.nanmean(permutation_group2))
        elif tail == 1:
            permdist[i] = np.nanmean(permutation_group1) - np.nanmean(permutation_group2)
    permdist = np.sort(permdist)
    if tail == 2:
        empdiff = abs(np.nanmean(dat1) - np.nanmean(dat2))
    elif tail == 1:
        empdiff = np.nanmean(dat1) - np.nanmean(dat2)
    p_value = sum(empdiff < permdist) / (pnum + 1)
    return p_value, permdist


# Get parcel info at stimsite and only if that parcel is included for the subject
df = pd.read_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t', index_col=0)
df = df[df['parcel_included_in_sub_mask']==True]
df = df[df['stimsite_issingleton']==0]

cart_profile_path = './esfmri_connectivity/analysis1/data/cartprofile/'
community_path = './esfmri_connectivity/communitydetection/data/'

# load community information
communities = {}
for sub in np.unique(df['subject'].values):
    communities[sub] = pd.read_csv(community_path + '/sub-' + str(sub) + '_task-es_communities.tsv', index_col=[0], sep='\t')

# load the PC and z for each run
cartprofile_eson = {}
cartprofile_esoff = {}
for i, row in df.iterrows():
    fname = 'sub-' + str(row['subject']) + '_ses-postop_task-es_run-' + str(row['run']).zfill(2) + '_desc-eson_cartprofile.tsv'
    cartprofile_eson[i] = pd.read_csv(cart_profile_path + fname, sep='\t', index_col=[0])
    fname = 'sub-' + str(row['subject']) + '_ses-postop_task-es_run-' + str(row['run']).zfill(2) + '_desc-esoff_cartprofile.tsv'
    cartprofile_esoff[i] = pd.read_csv(cart_profile_path + fname, sep='\t', index_col=[0])

# calculate the (1) max/median for (2) PC and z for (3) eson and esoff and (4) within and outside stimulation community
max_pc_eson_in = []
max_pc_esoff_in = []
max_z_eson_in = []
max_z_esoff_in = []
med_pc_eson_in = []
med_pc_esoff_in = []
med_z_eson_in = []
med_z_esoff_in = []
max_pc_eson_out = []
max_pc_esoff_out = []
max_z_eson_out = []
max_z_esoff_out = []
med_pc_eson_out = []
med_pc_esoff_out = []
med_z_eson_out = []
med_z_esoff_out = []
for i, row in df.iterrows():
    cid = int(communities[row['subject']].loc[int(row['overlapping_parcel_index'])].values)
    in_community = list(communities[row['subject']][communities[row['subject']]['communities'] == cid].index)
    out_community = list(communities[row['subject']][communities[row['subject']]['communities'] != cid].index)
    max_pc_eson_in.append(np.max(cartprofile_eson[i]['participation_coeff'].loc[in_community]))
    max_pc_esoff_in.append(np.max(cartprofile_esoff[i]['participation_coeff'].loc[in_community]))
    max_z_eson_in.append(np.max(cartprofile_eson[i]['within_module_degree_zscore'].loc[in_community]))
    max_z_esoff_in.append(np.max(cartprofile_esoff[i]['within_module_degree_zscore'].loc[in_community]))
    med_pc_eson_in.append(np.median(cartprofile_eson[i]['participation_coeff'].loc[in_community]))
    med_pc_esoff_in.append(np.median(cartprofile_esoff[i]['participation_coeff'].loc[in_community]))
    med_z_eson_in.append(np.median(cartprofile_eson[i]['within_module_degree_zscore'].loc[in_community]))
    med_z_esoff_in.append(np.median(cartprofile_esoff[i]['within_module_degree_zscore'].loc[in_community]))

    max_pc_eson_out.append(np.max(cartprofile_eson[i]['participation_coeff'].loc[out_community]))
    max_pc_esoff_out.append(np.max(cartprofile_esoff[i]['participation_coeff'].loc[out_community]))
    max_z_eson_out.append(np.max(cartprofile_eson[i]['within_module_degree_zscore'].loc[out_community]))
    max_z_esoff_out.append(np.max(cartprofile_esoff[i]['within_module_degree_zscore'].loc[out_community]))
    med_pc_eson_out.append(np.median(cartprofile_eson[i]['participation_coeff'].loc[out_community]))
    med_pc_esoff_out.append(np.median(cartprofile_esoff[i]['participation_coeff'].loc[out_community]))
    med_z_eson_out.append(np.median(cartprofile_eson[i]['within_module_degree_zscore'].loc[out_community]))
    med_z_esoff_out.append(np.median(cartprofile_esoff[i]['within_module_degree_zscore'].loc[out_community]))

# Calculate the displacement
disp_max_pc_in = np.array(max_pc_eson_in) - np.array(max_pc_esoff_in)
disp_max_pc_out = np.array(max_pc_eson_out) - np.array(max_pc_esoff_out)
disp_max_z_in = np.array(max_z_eson_in) - np.array(max_z_esoff_in)
disp_max_z_out = np.array(max_z_eson_out) - np.array(max_z_esoff_out)
disp_med_pc_in = np.array(med_pc_eson_in) - np.array(med_pc_esoff_in)
disp_med_pc_out = np.array(med_pc_eson_out) - np.array(med_pc_esoff_out)
disp_med_z_in = np.array(med_z_eson_in) - np.array(med_z_esoff_in)
disp_med_z_out = np.array(med_z_eson_out) - np.array(med_z_esoff_out)

df_displacement = pd.DataFrame(data={
    'run': df.run,
    'subject': df.subject,
    'disp_max_pc_in': disp_max_pc_in,
    'disp_max_pc_out': disp_max_pc_out,
    'disp_max_z_in': disp_max_z_in,
    'disp_max_z_out': disp_max_z_out,
    'disp_med_pc_in': disp_med_pc_in,
    'disp_med_pc_out': disp_med_pc_out,
    'disp_med_z_in': disp_med_z_in,
    'disp_med_z_out': disp_med_z_out
}, index=df.index)
df_displacement.to_csv('./esfmri_connectivity/analysis1/data/cartprofile/cartprofile_displacement.tsv', sep='\t')

# Non parameteric test to test whether the displacement within community is greater than displacement outside community
# tail = 1 as H-1 states the direction of the hypothesis
np.random.seed(2020)
n_permutations = 10000
tail = 1
p_pc_max, dist_pc_max = shufflegroups(np.array(disp_max_pc_in), np.array(disp_max_pc_out), n_permutations, tail=tail)
p_pc_med, dist_pc_med = shufflegroups(np.array(disp_med_pc_in), np.array(disp_med_pc_out), n_permutations, tail=tail)
p_z_max, dist_z_max = shufflegroups(np.array(disp_max_z_in), np.array(disp_max_z_out), n_permutations, tail=tail)
p_z_med, dist_z_med = shufflegroups(np.array(disp_med_z_in), np.array(disp_med_z_out), n_permutations, tail=tail)


test_label = ['max(PC)', 'median(PC)', 'max(z)', 'median(z)']
p_values = [p_pc_max, p_pc_med, p_z_max, p_z_med]
bonferroni_th_pvalues = np.array(p_values) < (0.05/len(p_values))

# Corrected p_value should be identical results to correcting cut off point of the distribution instead of correcting the p-value.
# But for a sanity check
cutoff = int(n_permutations - ((0.05/len(p_values))*n_permutations))
cutoff_vals = np.array([dist_pc_max[cutoff], dist_pc_med[cutoff], dist_z_max[cutoff], dist_z_med[cutoff]])
emp_vals = np.array([np.mean(np.array(disp_max_pc_in) - np.array(disp_max_pc_out)),
            np.mean(np.array(disp_med_pc_in) - np.array(disp_med_pc_out)),
            np.mean(np.array(disp_max_z_in) - np.array(disp_max_z_out)),
            np.mean(np.array(disp_med_z_in) - np.array(disp_med_z_out))])
bonferroni_th_cutoffvals = emp_vals > cutoff_vals
if not all(bonferroni_th_cutoffvals == bonferroni_th_pvalues):
    print('Correction methods give different thresholded results')

df_summary = pd.DataFrame(data={'test': test_label,
                        'p_values': p_values,
                        'under_0.05_thresholded_bonferroni': bonferroni_th_pvalues,
                        'displacement_avg_difference': emp_vals})
print(df_summary)
df_summary.to_csv('./esfmri_connectivity/analysis1/stats/summary.tsv', sep='\t')

df_permutations = pd.DataFrame(data={test_label[0]: dist_pc_max,
                        test_label[1]: dist_pc_med,
                        test_label[2]: dist_z_max,
                        test_label[3]: dist_z_med})
df_permutations.to_csv('./esfmri_connectivity/analysis1/stats/nonparametric_permuted_distributions.tsv', sep='\t')

# Plot results


sns.set_palette("pastel")

fig, ax = plt.subplots(2,2)
ax = ax.flatten()
data_pc = np.array([disp_max_pc_in, disp_max_pc_out,
        disp_med_pc_in, disp_med_pc_out])
data_z = np.array([disp_max_z_in, disp_max_z_out,
        disp_med_z_in, disp_med_z_out])
pos = [0, 1]

rel = np.hstack([np.tile('within', len(disp_max_pc_in)), np.tile('outside', len(disp_max_pc_out))])
data = pd.DataFrame(data={r'max $\Delta$ PC': np.hstack([disp_max_pc_in, disp_max_pc_out]), 'refstimsite': rel})
ax[0] = sns.violinplot(x="refstimsite", y=r'max $\Delta$ PC', data=data, inner=None, ax=ax[0], alpha=0.7)

rel = np.hstack([np.tile('within', len(disp_med_pc_in)), np.tile('outside', len(disp_med_pc_out))])
data = pd.DataFrame(data={r'median $\Delta$ PC': np.hstack([disp_med_pc_in, disp_med_pc_out]), 'refstimsite': rel})
ax[1] = sns.violinplot(x="refstimsite", y=r'median $\Delta$ PC', data=data, inner=None, ax=ax[1], alpha=0.7)

rel = np.hstack([np.tile('within', len(disp_max_z_in)), np.tile('outside', len(disp_max_z_out))])
data = pd.DataFrame(data={r'max $\Delta$ z': np.hstack([disp_max_z_in, disp_max_z_out]), 'refstimsite': rel})
ax[2] = sns.violinplot(x="refstimsite", y=r'max $\Delta$ z', data=data, inner=None, ax=ax[2], alpha=0.7)

rel = np.hstack([np.tile('within', len(disp_med_z_in)), np.tile('outside', len(disp_med_z_out))])
data = pd.DataFrame(data={r'median $\Delta$ z': np.hstack([disp_med_z_in, disp_med_z_out]), 'refstimsite': rel})
ax[3] = sns.violinplot(x="refstimsite", y=r'median $\Delta$ z', data=data, inner=None, ax=ax[3], alpha=0.7)


np.random.seed(2020)
for n in range(data_pc.shape[1]):
    ind = np.random.uniform(-0.075,0.075,1)
    ax[0].plot(pos + ind, data_pc[:2, n], 'o-', color='gray', ms=2, linewidth=0.2)
    ax[1].plot(pos + ind, data_pc[2:, n], 'o-', color='gray', ms=2, linewidth=0.2)

for n in range(data_z.shape[1]):
    ind = np.random.uniform(-0.075,0.075,1)
    ax[2].plot(pos + ind, data_z[:2, n], 'o-', color='gray', ms=2, linewidth=0.2)
    ax[3].plot(pos + ind, data_z[2:, n], 'o-', color='gray', ms=2, linewidth=0.2)

ax[0].scatter(pos, np.mean(data_pc[:2], axis=1), color='lightgray', zorder=100, s=15)
ax[1].scatter(pos, np.mean(data_pc[2:], axis=1), color='lightgray', zorder=100, s=15)
ax[2].scatter(pos, np.mean(data_z[:2], axis=1), color='lightgray', zorder=100, s=15)
ax[3].scatter(pos, np.mean(data_z[2:], axis=1), color='lightgray', zorder=100, s=15)

ax[0].set_ylim([-0.08, 0.13])
ax[1].set_ylim([-0.08, 0.13])
ax[2].set_ylim([-1, 1])
ax[3].set_ylim([-0.6, 0.7])


ax[0].set_yticks([-0.05, 0, 0.05, 0.1])
ax[1].set_yticks([-0.05, 0, 0.05, 0.1])
ax[2].set_yticks([-1, 0, 1])
ax[3].set_yticks([-0.5, 0, 0.5])

plotje.styler(ax[0], title='max PC', xlabel='Stimulation site\ncommunity', ylabel=r'$\Delta$ PC (es-on - es-off)', aspectsquare=True)
plotje.styler(ax[1],  xlabel='Stimulation site\ncommunity', title='median PC', ylabel=r'$\Delta$ PC (es-on - es-off)', aspectsquare=True)
plotje.styler(ax[2], title='max z', xlabel='Stimulation site\ncommunity', ylabel=r'$\Delta$ z (es-on - es-off)', aspectsquare=True)
plotje.styler(ax[3],  xlabel='Stimulation site\ncommunity', title='median z', ylabel=r'$\Delta$ z (es-on - es-off)', aspectsquare=True)


ax[0].set()
for a in ax:
    a.set_xlim([-0.5,1.5])
    a.set_xticks(pos)
    a.set_xticklabels(['Within', 'Outside'])
plt.tight_layout()

fig.savefig('./esfmri_connectivity/analysis1/figures/cartprofile_displacement.svg')
fig.savefig('./esfmri_connectivity/analysis1/figures/cartprofile_displacement.png', r=600)
