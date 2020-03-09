import nibabel as nib
import pandas as pd
from esfmri_connectivity.utils.getfiles import get_timeseries
import numpy as np

parc = nib.load('esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-01_atlas-smorgasbord_dseg.nii.gz')
stiminfo = pd.read_csv('./esfmri_connectivity/stimulation_sites/stimulation_infomation_space-MNI152NLin2009cAsym.tsv', sep='\t')

timeseries = get_timeseries(task='postop', require_stiminfo=True)

stim_center_mni = []
stim_center_xyz = []
for t in timeseries:
    sub = int(t.split('sub-')[1].split('_')[0])
    run = int(t.split('run-')[1].split('_')[0])
    # UNCLEAR IN PREREG
    # (stiminfo['multiple_contacts_in_run'] == 0, not specified in preregistration that subject will be excluded if multiple stimulations sites at once
    stim = stiminfo[(stiminfo['subject']==sub) & (stiminfo['run']==run) & (stiminfo['multiple_contacts_in_run'] == 0)]
    tmp = []
    stim_center_mni.append([np.round(np.mean([stim['contact1_mni_' + x].values, stim['contact2_mni_' + x].values]), 2) for x in ['x', 'y', 'z']])
    # centring on the voxel that best aligns with the coordinate and creating a sphere around that and great
    coord_xyz = np.linalg.inv(parc.affine).dot([stim_center_mni[-1][0], stim_center_mni[-1][1], stim_center_mni[-1][2], 1])[:-1]
    stim_center_xyz.append(np.round(coord_xyz.astype(int)))

def sphere(shape, radius, position):
    """
    taken from https://stackoverflow.com/questions/46626267/how-to-generate-a-sphere-in-3d-numpy-array/46626448
    """
    # assume shape and position are both a 3-tuple of int or float
    # the units are pixels / voxels (px for short)
    # radius is a int or float in px

    semisizes = (radius,) * 3

    # genereate the grid for the support points
    # centered at the position indicated by position
    grid = [slice(-x0, dim - x0) for x0, dim in zip(position, shape)]
    position = np.ogrid[grid]
    # calculate the distance of all points from `position` center
    # scaled by the radius
    arr = np.zeros(shape, dtype=float)
    for x_i, semisize in zip(position, semisizes):
        arr += (np.abs(x_i / semisize) ** 2)
    # the inner part of the sphere will have distance below 1
    return arr <= 1.0

# get_parcellation data
parc_data = parc.get_fdata()

best_roi = []
good_roi = []
sub = []
run = []
# DEVIATION FROM PREREG
# This was increased to 6 instead of 3 so all had some non-0 voxels.
# If this is less than 6, an error will occur as some subjects will have 0 throughout the sphere.
# Expanding the ROI seems to make sense, as multiple transforms have been applied and the centre of the roi is the middle of the two channels

roi_radius = 6
for i, xyz in enumerate(stim_center_xyz):
    sub.append(int(timeseries[i].split('sub-')[1].split('_')[0]))
    run.append(timeseries[i].split('run-')[1].split('_')[0])
    t = pd.read_csv(timeseries[i], sep='\t', index_col=[0])
    # Loop through all stimulations, make a sphere mask
    arr = sphere(parc.shape, roi_radius, xyz)
    # find the values withithe sphere
    vals = parc_data[arr]
    # exclude any 0s as these are not a roi
    vals = vals[vals!=0]
    # get counts of parcels overlapping with the sphere
    v, c = np.unique(vals, return_counts=True)
    # Find the parcel that overlaps the most
    best_roi.append(v[np.argmax(c)])
    #Check if stimulate parcel is in time series for subject
    if (v[np.argmax(c)] in t.index):
        good_roi.append(True)
    else:
        good_roi.append(False)

df = pd.DataFrame(data={'subject': sub, 'run': run, 'overlapping_parcel_index': best_roi, 'parcel_included_in_sub_mask': good_roi})

df.to_csv('./esfmri_connectivity/stimulation_sites/stimsite2parcel.tsv', sep='\t')