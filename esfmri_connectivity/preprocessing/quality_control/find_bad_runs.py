import bids
import pandas as pd
# Bad run is defined as any of the runs where the average movement was over 0.5
bids_dir = '/home/esfmri/esfmri_data/'
fmriprep_dir = 'derivatives/fmriprep-1.5.1/fmriprep/'
qa_dir = './esfmri_connectivity/preprocessing/quality_control/'

layout = bids.BIDSLayout(bids_dir)
layout.add_derivatives(bids_dir + fmriprep_dir)

# Loop over subjects cause pybids seems to have some memory issues to grab the tsvs at once. 
fmriprep_qa = pd.read_csv(qa_dir + 'fmriprep_evaluation.tsv', sep='\t')
subs = fmriprep_qa['sub'].values 
bad_runs = []
for s in subs:
    subfiles = layout.get(scope='fMRIPrep', subject=s.split('-')[1], desc='confounds', suffix='regressors', extension='tsv', return_type='file')
    for f in subfiles:
        confounds = pd.read_csv(f, sep='\t')
        if confounds['framewise_displacement'].mean() > 0.5:
            bad_runs.append(f.split('func')[1][1:].split('desc')[0][:-1])

bad_runs = pd.DataFrame(bad_runs)
bad_runs.to_csv(qa_dir + 'bad_runs.tsv', sep='\t')
