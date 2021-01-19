"""
The script adds whether there is a singleton or size-2 community to the stimsite2parcel tsv
"""
import pandas as pd
import numpy as np

df = pd.read_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t')

community_path = './esfmri_connectivity/communitydetection/data/'

# load community information
stimsitesingleton = []
for _, row in df.iterrows():
    if row['parcel_included_in_sub_mask']==True:

        coms = pd.read_csv(community_path + '/sub-' + str(row['subject']) + '_task-es_communities.tsv', index_col=[0], sep='\t')
        stimsite = coms['communities'].loc[row['overlapping_parcel_index']]
        stimsitecomsize = np.sum(coms['communities']==stimsite)
        if stimsitecomsize < 3:
            stimsitesingleton.append(1)
        else:
            stimsitesingleton.append(0)
    else: 
        stimsitesingleton.append(np.nan)

df['stimsite_issingleton'] = stimsitesingleton
df.to_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t')
