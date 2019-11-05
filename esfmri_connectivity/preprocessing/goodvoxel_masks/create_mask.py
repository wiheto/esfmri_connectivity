import nibabel as nib
from nilearn.image.resampling import resample_to_img
from sklearn.mixture import GaussianMixture
import numpy as np
import pandas as pd
import os
parc = nib.load(
    './esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-02_atlas-frankenstein_dseg.nii.gz')
parcdata = parc.get_data()

parcinfo = pd.read_csv(
    './esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-01_atlas-frankenstein_dseg.tsv', sep='\t', index_col=[0])

rel_dir = './esfmri_connectivity/preprocessing/goodvoxel_masks/'

c = 4
files = os.listdir(rel_dir + 'avg_voxel_distribution')
files = [f for f in files if f.endswith('_voxdist.npy')]
report = []
sub = []
task = []
for f in files:
    data = np.load(rel_dir + 'avg_voxel_distribution/' + f)
    data = np.array(data, ndmin=2).transpose()
    fitted_gm = GaussianMixture(c, random_state=2019)
    fitted_gm.fit(data)
    predicted_gm = fitted_gm.predict(data)
    # reject the lowest mean
    nontarget = np.argmin(fitted_gm.means_)

    # Step 1 is to make all the "bad voxels" 0
    goodvoxels = predicted_gm != nontarget
    ind = np.where(parcdata != 0)
    badx = ind[0][~goodvoxels]
    bady = ind[1][~goodvoxels]
    badz = ind[2][~goodvoxels]
    maskparc = parcdata.copy()
    maskparc[badx, bady, badz] = np.nan

    # Step 2, check how much of each parcel remains.
    n = 0
    parcinmask = []
    for parcel in np.unique(parcdata[ind]):
        inmask = np.sum(maskparc == parcel)
        intemplate = np.sum(parcdata == parcel)
        if (inmask/intemplate) < 0.5:
            maskparc[maskparc == parcel] = np.nan
            n += 1
            parcinmask.append(0)
        else:
            parcinmask.append(1)
    maskinfo = pd.DataFrame(
        data={'name': parcinfo['name'], 'inmask': parcinmask})
    print(str(n) + ' parcels deleted')
    report.append(n)
    # Save output
    maskimg = nib.Nifti1Image(maskparc, parc.affine)
    nib.save(maskimg, rel_dir + 'masks/' + f.split('_voxdist')
             [0] + '_tpl-MNI152NLin2009cAsym_res-02_atlas-frankenstein_dseg.nii.gz')
    maskinfo.to_csv(rel_dir + 'masks/' + f.split('_voxdist')
                    [0] + '_tpl-MNI152NLin2009cAsym_res-02_atlas-frankenstein_dseg.tsv', sep='\t')
    s, t, _ = f.split('_')
    sub.append(s)
    task.append(t)

report = pd.DataFrame(
    data={'sub': sub, 'task': task, 'parcels_deleted': report})
report.to_csv(rel_dir + 'parceldelete_report.tsv', sep='\t')
