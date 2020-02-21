# Smörgåsbord Parcellation

A custom parcellation (aka Smörgåsbord) is made using:

1.  Schaeffer 400 cortical parcellation
2.  Oxford Harvard subcortical
3.  3 ROI Amygdala atlas
4.  10 ROI cerbebellum atlas

In each folder you will find how 2-4 is created. Number 1 is pulled directly from templateflow.

To fully replicate the analyses from scratch, you need to perform all the steps in the subdirectories of this folder first (any order). However all files are provided in those directories as well.

## Directory contents

This folder contains the "Smörgåsbord" atlas that we created for this analysis (because we merged multiple atlases).

The atlas label file:

`tpl-MNI152NLin2009cAsym_res-01_atlas-smorgasbord_dseg.nii.gz`

The information about the parcels:

`tpl-MNI152NLin2009cAsym_res-01_atlas-smorgasbord_dseg.tsv`

And to recreate these files you need:

`create_parcellation.py`

To run this file with the docker image simply type:

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.parcellation.create_parcellation`
