import templateflow.api as tf
import nibabel as nib
import pandas as pd
import numpy as np

# Specify save path
rel_path = './esfmri_connectivity/parcellation/'

# Download Scaeffer400 atlas
data = {}
data_path = tf.get('MNI152NLin2009cAsym', resolution=1,
                   atlas='Schaefer2018', desc='400Parcels7Networks', extension='.nii.gz')
img_cortex = nib.load(str(data_path))
data['cortex'] = img_cortex.get_data().astype(float)

info_path = tf.get('MNI152NLin2009cAsym', atlas='Schaefer2018', desc='400Parcels7Networks', extension='tsv')
info_cortex = pd.read_csv(str(info_path), sep='\t', index_col=[0])

# Load cerebellum

img_cerebellum = nib.load(rel_path + 'cerebellum/tpl-MNI152NLin2009cAsym_res-01_atlas-King2019Cerebellum_dseg.nii.gz')
data['cerebellum'] = img_cerebellum.get_data().astype(float)
info_cerebellum = pd.read_csv(rel_path + 'cerebellum/tpl-MNI152NLin2009cAsym_res-01_atlas-King2019Cerebellum_dseg.tsv', sep='\t', index_col=[0])
# Remove background/0 from this dataframae
info_cerebellum.drop(0, inplace=True)

# Load amygdala

img_amygdala = nib.load(rel_path + 'amygdala/tpl-MNI152NLin2009cAsym_res-01_atlas-3roiamygdala_dseg.nii.gz')
data['amygdala'] = img_amygdala.get_data().astype(float)
info_amygdala = pd.read_csv(rel_path + 'amygdala/tpl-MNI152NLin2009cAsym_res-01_atlas-3roiamygdala_dseg.tsv', sep='\t', index_col=[0])

# Load subcortical

img_subcortical = nib.load(rel_path + 'subcortical/tpl-MNI152NLin2009cAsym_res-01_atlas-HOSPA_desc-th50_dseg.nii.gz')
data['subcortical'] = img_subcortical.get_data().astype(float)
info_subcortical = pd.read_csv(rel_path + 'subcortical/tpl-MNI152NLin6Asym_atlas-HOSPA_dseg.tsv', sep='\t', index_col=[0])


# Check that there is no overlap in the different dictionaries
def calc_number_of_voxels_per_parcel(img, info):
    number_of_voxels = []
    for n in info.index:
        number_of_voxels.append(np.sum(img==n))
    return pd.DataFrame(number_of_voxels, index=info.index)

n_cortex = calc_number_of_voxels_per_parcel(data['cortex'], info_cortex)
n_amygdala = calc_number_of_voxels_per_parcel(data['amygdala'], info_amygdala)
n_subcortical = calc_number_of_voxels_per_parcel(data['subcortical'], info_subcortical)
n_cerebellum = calc_number_of_voxels_per_parcel(data['cerebellum'], info_cerebellum)

data_mod = {}
for i, d in enumerate(data.keys()):
    data_mod[d] = data[d].copy()
    for ii, dd in enumerate(data.keys()):
        if i != ii:
            x = np.where(data[d].flatten()>0)[0]
            y = np.where(data[dd].flatten()>0)[0]
            intersec = set(x).intersection(y)
            tmp = data_mod[d].flatten()
            tmp[list(intersec)] = 0
            data_mod[d] = tmp.reshape(data_mod[d].shape)
            if len(intersec) > 0:
                print('intersection: ' + d + ' and ' + dd + ': ' + str(len(intersec)))

m_cortex = calc_number_of_voxels_per_parcel(data_mod['cortex'], info_cortex)
m_amygdala = calc_number_of_voxels_per_parcel(data_mod['amygdala'], info_amygdala)
m_subcortical = calc_number_of_voxels_per_parcel(data_mod['subcortical'], info_subcortical)
m_cerebellum = calc_number_of_voxels_per_parcel(data_mod['cerebellum'], info_cerebellum)

data_mod['cerebellum'] += 400
data_mod['cerebellum'][data_mod['cerebellum'] == 400] = 0
info_cerebellum.index += 400

data_mod['subcortical'] += 500
data_mod['subcortical'][data_mod['subcortical'] == 500] = 0
info_subcortical.index += 500

data_mod['amygdala'] += 600
data_mod['amygdala'][data_mod['amygdala'] == 600] = 0
info_amygdala.index += 600



data_frank = data_mod['cortex'].copy()
data_frank += data_mod['amygdala']
data_frank += data_mod['cerebellum']
data_frank += data_mod['subcortical']

img_frank = nib.Nifti1Image(data_frank, img_cortex.affine)
savename = 'tpl-MNI152NLin2009cAsym_res-01_atlas-frankenstein_dseg'
nib.save(img_frank, rel_path + savename + '.nii.gz')

info_frank = pd.concat([info_cortex, info_cerebellum, info_subcortical, info_amygdala], sort=True)
info_frank.to_csv(rel_path + savename + '.tsv', sep='\t')
