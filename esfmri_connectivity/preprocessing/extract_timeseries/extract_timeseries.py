from nilearn.input_data import NiftiLabelsMasker
from esfmri_connectivity.utils.getfiles import get_preproc_files
import pandas as pd
import bids
import numpy as np
import os
# Where the data is
bids_dir = '/home/william/sherlock/scratch/data/esfmri/'
derivative_dir = 'derivatives/fmridenoise/'
fmriprep_dir = 'derivatives/fmriprep-1.5.1/fmriprep/'
pipeline = '24HMP_aCompCor_SpikeReg_4GSR'
rel_path = './esfmri_connectivity/'
mask_path = rel_path + 'preprocessing/goodvoxel_masks/masks/'
save_path = rel_path + 'timeseries/'

files = get_preproc_files(bids_dir, derivative_dir, pipeline=pipeline)

layout = bids.BIDSLayout(bids_dir)
layout.add_derivatives(bids_dir + fmriprep_dir)

for f in files:
    print(f)
    sub = 'sub' + f.split('/')[-1].split('sub')[1].split('_')[0]
    task = 'task' + f.split('/')[-1].split('task')[1].split('_')[0]
    sname = f.split('/')[-1]
    sname = sname.split('_desc')[0]
    sname += '_timeseries.tsv'
    scrubbed_sname = sname.split('_timeseries')[0]
    scrubbed_sname += '_desc-fdcensored_timeseries.tsv'
    if not os.path.exists(save_path + scrubbed_sname):
        maskfile = mask_path + sub + '_' + task + \
            '_tpl-MNI152NLin2009cAsym_res-02_atlas-frankenstein_dseg.nii.gz'
        maskinfo = pd.read_csv(mask_path + sub + '_' + task +
                            '_tpl-MNI152NLin2009cAsym_res-02_atlas-frankenstein_dseg.tsv', sep='\t', index_col=0)
        mask = NiftiLabelsMasker(maskfile)
        timeseries = mask.fit_transform(f)
        if maskinfo['inmask'].sum() != timeseries.shape[1]:
            raise ValueError('Wrong/Unexpected dimensions')
        # Index corresponds to maskfile index
        timeseries = pd.DataFrame(timeseries.transpose(
        ), index=maskinfo[maskinfo['inmask'] == 1].index)
        timeseries.to_csv(save_path + sname, sep='\t')

        confounds = layout.get(scope='fMRIPrep', subject=sub.split('-')[1], task=task.split('-')[1], run=int(
            f.split('run-')[1].split('_')[0]), desc='confounds', suffix='regressors', extension='tsv', return_type='file')
        if len(confounds) != 1:
            raise ValueError('Unexpected number of confound files grabbed')
        df = pd.read_csv(confounds[0], sep='\t')
        badtimepoints = list(df[df['framewise_displacement'] > 0.5].index)
        scrubbed_timeseries = timeseries.copy()
        # Set entire column to nan of time that are bad.
        scrubbed_timeseries[badtimepoints] = np.nan
        scrubbed_timeseries.to_csv(save_path + scrubbed_sname, sep='\t')
