import templateflow.api as tf
import nibabel as nib
import pandas as pd
import numpy as np

rel_path = './esfmri_connectivity/parcellation/subcortical/'

unwanted_indicies = [1,2,3, 10, 12,13,14,20]

data_path = tf.get('MNI152NLin2009cAsym', resolution=1,
                   atlas='HOSPA', desc='th50', extension='.nii.gz')
img = nib.load(str(data_path))
data = img.get_data()
# set amgydala, white mater, cerebral cortex and ventricals values to zero
for i in unwanted_indicies:
    data[data == i] = 0
new_img = nib.Nifti1Image(data, img.affine)
nib.save(new_img, rel_path + data_path.name)

info_path = tf.get('MNI152NLin6Asym', atlas='HOSPA', extension='tsv')
info = pd.read_csv(str(info_path), sep='\t', index_col=[0])
# Add brain steam
info.loc[7] = ['Brainstem', '44, 49, 18']
info = info.sort_index()
# Fix index to start at 1
info.index = np.arange(1, len(info)+1)
# Remove amygdala
info = info.drop(unwanted_indicies)
info.to_csv(rel_path + info_path.name, sep='\t')
