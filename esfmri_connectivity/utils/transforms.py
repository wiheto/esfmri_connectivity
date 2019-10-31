from nipype.interfaces.ants import ApplyTransforms
import shutil
def antstransform(path, inimage, reference, transform, outimage, interpolation='MultiLabel'):
    at = ApplyTransforms()
    # Input: image to change in FSL
    at.inputs.input_image = path + inimage
    # Ref
    at.inputs.reference_image = str(reference)
    # transform-file.
    at.inputs.transforms = str(transform)
    at.inputs.interpolation = interpolation
    at.run()

    ants_output_name = inimage.split('.')[0] + '_trans.nii.gz'
    shutil.move(ants_output_name, path + outimage)