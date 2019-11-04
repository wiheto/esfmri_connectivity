import bids
import pandas as pd

# Utilizing pybids to get all files that are marked as "good"


def get_preproc_files(bids_dir, fmriprep_dir, qa_path='./esfmri_connectivity/preprocessing/quality_control/', pipeline=None, forceonehit=True):

    qa = pd.read_csv(qa_path + 'fmriprep_evaluation.tsv', sep='\t')
    bad_subs = qa['sub'][qa['use'] == 0].values
    bad_runs = qa.dropna(subset=['reject_runs'])

    bad_runs_movement = pd.read_csv(qa_path + 'bad_runs.tsv', sep='\t')

    layout = bids.BIDSLayout(bids_dir)
    layout.add_derivatives(bids_dir + fmriprep_dir)

    get_all = layout.get(scope='derivatives', desc='preproc',
                         extension='nii.gz', space='MNI152NLin2009cAsym')

    # remove all bad subjects
    filepaths = [n.dirname + '/' + n.filename for n in get_all]
    # make sure bold is in the name (cant be in lay due to fmridenoise)
    filepaths = [f for f in filepaths if 'bold' in f]
    for bs in bad_subs:
        filepaths = list(filter(lambda x: bs not in x, filepaths))
    if pipeline is not None:
        filepaths = [f for f in filepaths if 'pipeline-' + pipeline + '.' in f]
    # remove all bad runs from manual evaluation
    for _, br in bad_runs.iterrows():
        reject_runs = br['reject_runs'].split(',')
        sub = br['sub']
        for taskrun in reject_runs:
            if taskrun == '':
                pass
            elif sub not in bad_subs:
                task, run = taskrun.split('_')
                l1 = len(filepaths)
                toremove = list(
                    filter(lambda x: sub in x and run in x and task in x, filepaths))
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

    # remove all bad runs with high movement
    bad_runs_hm = list(bad_runs_movement['high_movement_runs'].values)
    filepaths = list(filter(lambda x: not any(list(filter(
        lambda y: y in x, bad_runs_hm))), filepaths))

    return filepaths
