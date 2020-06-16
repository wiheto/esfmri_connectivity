import nibabel as nib
import pandas as pd
import numpy as np


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

label = {}

sub = '292'
label['sub'] = {}
com = pd.read_csv(com_path + 'sub-' + sub + '_task-es' + '_communities.tsv', sep='\t', index_col=[0])


for c in com['communities'].unique()
    c_alt = template.loc[(com['communities'] == c).index]['comname'].values
    net, counts = np.unique(c_alt, return_counts=True)
    counts = counts/len(c_alt)
    label['sub'][c] = net[np.argmax(counts)]
    