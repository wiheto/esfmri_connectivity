import bids
import pandas as pd
import os
import nibabel as nib
import numpy as np


def get_timeseries(timeseries_dir='./esfmri_connectivity/timeseries', task=None, censored=True, group=None):
    files = os.listdir(timeseries_dir)
    if censored == True:
        files = [timeseries_dir + '/' + f for f in files if 'fdcensored' in f]
    else:
        files = [timeseries_dir + '/' +
                 f for f in files if 'fdcensored' not in f]
    if task is not None: 
        files = [f for f in files if task in f]
    if group == 'subtask':
        pairings = [('sub-' + f.split('/')[-1].split('sub-')[1].split('_')[0],
                     'task-' + f.split('/')[-1].split('task-')[1].split('_')[0]) for f in files]
        pairings = list(set(pairings))
        files_col = []
        labels = []
        for p in pairings:
            files_col.append([f for f in files if p[0] in f and p[1] in f])
            labels.append('_'.join(p))
        files = files_col
        return files, labels
    else:
        return files


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


def get_events(bids_dir, subject, run, reject=5, return_type='block'):
    """
    Returns the index of stim on and stim off time periods.
    Should pass a subject and run that returns a unique file.
    Reject variable is the number of seconds at the start of each block that are removed.
    return_type can be block or run.
    """
    layout = bids.BIDSLayout(bids_dir)
    # Get both events and images, check there is only one of each
    events = layout.get(suffix='events', extension='.tsv', session='postop',
                        return_type='file', subject=subject, run=int(run))
    images = layout.get(suffix='bold', extension='.nii.gz', session='postop',
                        return_type='file', subject=subject, run=int(run))
    if (len(events) != len(images)) and (len(events) != 1):
        raise ValueError(
            'Different number of events, json, or image files found.')
    # load events and image
    ev = pd.read_csv(events[0], sep='\t')
    img = nib.load(images[0])
    # Get the tr
    tr = img.header.get_zooms()[-1]
    # How many seconds to delete from each of the "blocks/trials"
    delete_from_start = np.ceil(reject/tr)
    seconds = np.arange(0, img.shape[-1]*tr, tr)
    # Define stim on and stim off periods in seconds
    stimon = np.sort(
        np.array(list(set(seconds).intersection(ev['onset'].round()))))
    stimoff = np.sort(
        np.array(list(set(seconds).difference(ev['onset'].round()))))
    # Fine where the stimulation is greater than the tr to find where a block ends
    lps = np.where(np.diff(stimon) > tr)[0]
    lastpoints = [lps + lp for lp in np.arange(1, 1+delete_from_start)]
    lastpoints.append(np.arange(delete_from_start))
    to_delete = np.sort(np.concatenate(lastpoints))
    delstimon = np.delete(stimon, to_delete.astype(int))
    # Do same for stim off
    lps = np.where(np.diff(stimoff) > tr)[0]
    lastpoints = [lps + lp for lp in np.arange(1, 2+delete_from_start)]
    lastpoints.append(np.arange(delete_from_start+1))
    to_delete = np.sort(np.concatenate(lastpoints))
    delstimoff = np.delete(stimoff, to_delete.astype(int))
    # Convert back to frames
    stimon_frames = (delstimon/tr).astype(int)
    stimoff_frames = (delstimoff/tr).astype(int)
    # If return per block, split up into list of multiple arrays
    if return_type == 'block':
        stimon_frames = np.split(stimon_frames, np.where(
            np.diff(stimon_frames) > 1)[0]+1)
        stimoff_frames = np.split(stimoff_frames, np.where(
            np.diff(stimoff_frames) > 1)[0]+1)

    return stimon_frames, stimoff_frames
