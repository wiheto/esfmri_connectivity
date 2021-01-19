"""
Used in supplementary figure. 
Assigns a label from the Yeo 7 atlas to each of the communities for each subject. 
Note, this is only a quick estimate.
"""

import nibabel as nib
import pandas as pd
import numpy as np
import os

template = pd.read_csv('esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-01_atlas-smorgasbord_dseg.tsv', sep='\t', index_col=[0])

cortex = template[template.index <= 400]
subcortex = template[template.index > 400]

namelist = {}
template_community = []
for c in cortex['name']:
    name = c.split('_')[2]
    if name not in namelist.keys():
        namelist[name] = name
    template_community.append(namelist[name])

for c in subcortex['name']:
    template_community.append('subcortical')

template['comname'] = template_community

com_path = './esfmri_connectivity/communitydetection/data/'

files = os.listdir(com_path)
files = [f for f in files if 'task-es' in f and 'communities' in f]

for f in files:

    sub = f.split('_')[0].split('-')[1]
    label = {}
    com = pd.read_csv(com_path + 'sub-' + sub + '_task-es' + '_communities.tsv', sep='\t', index_col=[0])

    for c in com['communities'].unique():
        c_alt = template.loc[com[com['communities'] == c].index]['comname'].values
        net, counts = np.unique(c_alt, return_counts=True)
        counts = counts/len(c_alt)
        label[c] = net[np.argmax(counts)]
    df = pd.Series(label)
    df.to_csv(com_path + 'sub-' + sub + '_task-es_labels.tsv', sep='\t')