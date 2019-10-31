# Amygdala atlas

## Attribution and licence of the cerebellum atlas

Tyszka, J. M. & Pauli, W. M. (2016) [In vivo delineation of subdivisions of the human amygdaloid complex in a high-resolution group template](https://onlinelibrary.wiley.com/doi/abs/10.1002/hbm.23289). Human Brain Mapping. 37, 3979–3998

The amygdala atlas files are shared under the [CC-By Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) and this licence applies to them here. Read more info [here](https://osf.io/hksa6/)

## How to recreate the files in this directory

All the files that are needed in this project are provided in this directory.

## Step 1: Download the files

The file CIT168_pAmyNuc_1mm_MNI.nii.gz was downloaded from [here](https://osf.io/5ujaf/).

The CIT168_AmyLabels.txt file was downloaded [here](https://osf.io/ngxtw/)

Save both these files into this directory.

## Step 2: Reduce to 3 ROIs and make discrete

Create a filename compatible with templateflow's naming structure:

`docker run -u `id -u` -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.parcellation.amygdala.combine_rois`

This file uses the probabilistic Amygdala atlas and creates 3 discrete ROIs. It also exports the metainfo.

## Step 3: convert to MNI152NLin2009cAsym

We will then convert the Amygdala atlas into MNI152NLin2009cAsym and give it a templateflow-like name:

`docker run -u `id -u` -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.parcellation.amygdala.reref_mniNLin6_to_mni2009c`

This will create:

`tpl-MNI152NLin2009cAsym_res-01_atlas-3roiamygdala_dseg.nii.gz`

in this directory.