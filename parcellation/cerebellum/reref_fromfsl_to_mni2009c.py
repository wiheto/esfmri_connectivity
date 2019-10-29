from nipype.interfaces.ants import ApplyTransforms
import templateflow.api as tf
import shutil

relpath = './parcellation/cerebellum/'

transform = tf.get(template='MNI152NLin2009cAsym', suffix='xfm', extension='h5')
reference = tf.get(template='MNI152NLin2009cAsym', suffix='T1w', resolution=1, desc='brain', extension='nii.gz')

#img path
imgs = ['tpl-MNI152NLin6Asym_res-01_atlas-King2019Cerebellum_dseg.nii.gz']
out_imgs = [relpath + 'tpl-MNI152NLin2009cAsym_res-01_atlas-King2019Cerebellum_dseg.nii.gz']

for n, i in enumerate(imgs):
    at = ApplyTransforms()
    # Input: image to change in FSL
    at.inputs.input_image = relpath + i
    # Ref
    at.inputs.reference_image = str(reference)
    # transform-file.
    at.inputs.transforms = str(transform)
    at.inputs.interpolation = 'MultiLabel'
    at.run()

    shutil.move(i.split('.')[0] + '_trans.nii.gz', out_imgs[n])