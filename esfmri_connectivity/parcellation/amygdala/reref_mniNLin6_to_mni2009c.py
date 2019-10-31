import templateflow.api as tf
from ...utils import transforms

relpath = './esfmri_connectivity/parcellation/amygdala/'

transform = tf.get(template='MNI152NLin2009cAsym', suffix='xfm', extension='h5')
reference = tf.get(template='MNI152NLin2009cAsym', suffix='T1w', resolution=1, desc='brain', extension='nii.gz')

#img path
imgs = ['tpl-MNI152NLin6Asym_res-01_atlas-3roiamygdala_dseg.nii.gz']
out_imgs = ['tpl-MNI152NLin2009cAsym_res-01_atlas-3roiamygdala_dseg.nii.gz']

for n, i in enumerate(imgs):
    transforms.antstransform(relpath, i, reference, transform, out_imgs[n])

