import os
import numpy as np 
from esfmri_connectivity.utils.getfiles import get_preproc_files
import nibabel as nib
from nilearn.image.resampling import resample_to_img


# Where the data is
bids_dir = '/home/william/sherlock/scratch/data/esfmri/'
fmriprep_dir = 'derivatives/fmriprep-1.5.1/fmriprep'
files = get_preproc_files(bids_dir, fmriprep_dir, pipeline=None)

# Get unique subjects
subjects = [f.split('sub-')[1].split('/')[0] for f in files]
subjects = list(np.unique(subjects))

# Get unique tasks
task = [f.split('task-')[1].split('_')[0] for f in files]
task = list(np.unique(task))


# Resample frankenstein atlas to make it correct resolution of data
parc = nib.load('./esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-01_atlas-frankenstein_dseg.nii.gz')
exfunc = nib.load(files[0])
rsparc = resample_to_img(parc, exfunc, interpolation='nearest')
nib.save(rsparc, './esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-02_atlas-frankenstein_dseg.nii.gz')

parcdata = rsparc.get_data()
ind = np.where(parcdata != 0)




for s in subjects:
    print(s)
    for t in task:
        if not os.path.exists('./esfmri_connectivity/preprocessing/goodvoxel_masks/avg_voxel_distribution/sub-' + s + '_task-' + t + '_voxdist.npy'): 
            # Get files of specific subject/task
            st_files = [f for f in files if s in f and 'task-' + t in f]
            if len(st_files) > 0: 
                data = []
                for run in st_files: 
                    img = nib.load(run)
                    if rsparc.shape != img.shape[:3]: 
                        raise ValueError('Images are different shapes')
                    tmp = img.get_data()
                    tmp = tmp[ind[0], ind[1], ind[2], :]
                    data.append(tmp)
                data = np.concatenate(data, axis=1)
                data = np.mean(data, axis=1)
                print(data.mean())
                np.save('./esfmri_connectivity/preprocessing/goodvoxel_masks/avg_voxel_distribution/sub-' + s + '_task-' + t + '_voxdist.npy', data)




