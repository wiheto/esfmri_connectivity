import pandas as pd
import nibabel as nib
import numpy as np

relpath = 'esfmri_connectivity/parcellation/amygdala/'
img = nib.load(relpath + 'CIT168_pAmyNuc_1mm_MNI.nii.gz')

# Taken from relpath/CIT168_AmyLabels.txt

labels = ['AMY_BLN_La', 'AMY_BLN_BL_BLD+BLI', 'AMY_BLN_BM', 'AMY_CEN',
          'AMY_CMN', 'AMY_BL_BLV', 'AMY_ATA', 'AMY_ATA_ASTA', 'AMY_AAA', 'AMY']

# From correspondence, these are the three groupings:

labelinfo = pd.DataFrame(data={'labels': labels},
                         index=np.arange(1, len(labels)+1))


# Central:
target = ['AMY_CEN']
ind = list(labelinfo[labelinfo['labels'].isin(target)].index)
central_roi = np.squeeze(img.get_data()[:, :, :, ind])

# Corticomedial:
target = ['ThreAMY_CMN', 'AMY_AAA']
ind = list(labelinfo[labelinfo['labels'].isin(target)].index)
corticomedial_roi = np.sum(img.get_data()[:, :, :, ind], axis=-1)

# Basolateral:
target = ['AMY_BLN_BL_BLD+BLI', 'AMY_BLN_BM', 'AMY_BL_BLV']
ind = list(labelinfo[labelinfo['labels'].isin(target)].index)
basolateral_roi = np.sum(img.get_data()[:, :, :, ind], axis=-1)

# Create new roi by enforcing the roi with the highest probability to be discrete
new_rois = np.zeros(img.shape[:-1])
new_rois[(central_roi > corticomedial_roi) & (
    central_roi > basolateral_roi) & (central_roi > 0.25)] = 1
new_rois[(corticomedial_roi > central_roi) & (corticomedial_roi >
                                              basolateral_roi) & (corticomedial_roi > 0.25)] = 2
new_rois[(basolateral_roi > central_roi) & (basolateral_roi >
                                            corticomedial_roi) & (basolateral_roi > 0.25)] = 3

# Now with the discrete images we need to split L vs R
# Make everything in the R side + 10
new_rois[int(img.affine[0, -1]):] += 10
new_rois[new_rois == 10] = 0
new_rois[new_rois == 11] = 4
new_rois[new_rois == 12] = 5
new_rois[new_rois == 13] = 6

# Make nifti
new_img = nib.Nifti1Image(new_rois, img.affine)
nib.save(new_img, relpath +
         'tpl-MNI152NLin6Asym_res-01_atlas-3roiamygdala_dseg.nii.gz')

# Make metadata for dseg:ed image
names = ['amygdala_central_left', 'amygdala_corticomedial_left', 'amygdala_basolateral_left',
         'amygdala_central_right', 'amygdala_corticomedial_right', 'amygdala_basolateral_right']
abbr = ['AMY_CEN_L', 'AMY_CM_L', 'AMY_BL_L',
        'AMY_CEN_R', 'AMY_CM_R', 'AMY_BL_R']
metainfo = pd.DataFrame(
    data={'name': names, 'abbr': abbr}, index=[1, 2, 3, 4, 5, 6])
metainfo.to_csv(
    relpath + 'tpl-MNI152NLin6Asym_res-01_atlas-3roiamygdala_dseg.tsv', sep='\t')
metainfo.to_csv(
    relpath + 'tpl-MNI152NLin2009cAsym_res-01_atlas-3roiamygdala_dseg.tsv', sep='\t')
