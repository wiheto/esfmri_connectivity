import bids
import pandas as pd

## Utilizing pybids to get all files that are marked as "good"
def get_files(bids_dir, fmriprep_dir, qa_path, pipeline=None, forceonehit=True):

    qa = pd.read_csv(qa_path, sep='\t')
    bad_subs = qa['sub'][qa['use']==0].values
    bad_runs = qa.dropna(subset=['reject_runs'])

    layout = bids.BIDSLayout(bids_dir)
    layout.add_derivatives(bids_dir + fmriprep_dir)

    get_all = layout.get(scope='derivatives', desc='preproc', extension='nii.gz', space='MNI152NLin2009cAsym')

    ## remove all subjects
    filepaths = [n.dirname + '/' + n.filename for n in get_all]
    for bs in bad_subs:
        filepaths = list(filter(lambda x : bs not in x, filepaths))
    if pipeline is not None:
        filepaths = [f for f in filepaths if 'pipeline-' + pipeline + '.' in f]
    ## remove all bad runs
    for _, br in bad_runs.iterrows():
        reject_runs = br['reject_runs'].split(',')
        sub = br['sub']
        for taskrun in reject_runs:
            if taskrun == '':
                pass
            elif sub not in bad_subs:
                task, run = taskrun.split('_')
                l1 = len(filepaths)
                toremove = list(filter(lambda x : sub in x and run in x and task in x, filepaths))
                if len(toremove) > 1 and forceonehit:
                    raise ValueError('more than 2 files found to remove')
                elif len(toremove) == 0:
                    # Some derivatives files manually deleted due to get fmridenoise to run
                    pass
                else:
                    _ = [filepaths.remove(r) for r in toremove]
                    l2 = len(filepaths)
                    # Checks to make sure a file is removed and only one file
                    if l1 == l2:
                        raise ValueError('No run removes')
                    if (l1 != l2 + 1) and forceonehit:
                        raise ValueError('More than one run removed')

    return filepaths
