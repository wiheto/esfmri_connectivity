# es-fMRI connectivity

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/20435b80c0ed49f7bdf5341a65ad7ff6)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=wiheto/esfmri_connectivity&utm_campaign=Badge_Grade)

All code for the project: Functional connectivity of the human brain investigated using concurrent electrical stimulation and fMRI

OSF link: <https://osf.io/pdhfu/>

## Organization (while work is ongoing)

-   Issues contain elements of the preregistration that are to be done. 
-   Each issue is assigned to a project. 
-   Code for each project gets placed in ./projectname/ directory

## Code

Each projects code

-   ./esfmri_connectivity/projectname/

In the README of each directory it should be clearly stated which data it is acting on and contain a list or execution order. If a Dockerfile has been used for a specific part of the analysis (e.g. fMRIPrep) this should be stated. If nothing is specified, then the main ./Dockerfile is used.  

## List of docker commands to replicate project. 

This is a list of docker commands using the docker container of this repository. This assumes that fMRIPrep and fMRIDenoise have been run. To replicate those steps see `./preprocessing/fmriprep/README.md` and `./preprocessing/fmridenoise/README.md`. 

Next, navigate to this repositories main directory (where this README file is). This is wto be the working directory when rerunning the commaned.

Next, set the bash variable `ESFMRI_DATA` to point to where the BIDS directory is.

`ESFMRI_DATA='path/to/data'`

It also assumes the fMRIPrep and fMRIdenoise is saved in: 

`$ESFMRI_DATA/derivatives/fmriprep-1.5.1/fmriprep/`
`$ESFMRI_DATA/derivatives/denoise/`

This is the output if following the steps above.  

### Create Smörgåsbord parcellation

The parcellation used is included within the repo. But to replicate all the steps to recreate the parcellation see:

- Amygdala - see: `./esfmri_connectivity/parcellation/amygdala/README.md`
- Cerebellum - see: `./esfmri_connectivity/parcellation/cerebellum/README.md`
- Subcortical - see: `./esfmri_connectivity/parcellation/cerebellum/README.md`
- Create Smörgåsbord parcellation - see `./esfmri_connectivity/parcellation/README.md`

### Preprocessing steps

#### Find the bad runs with exceesive movement

`docker run -u esfmri -v $(pwd):/home/esfmri/ -v $ESFMRI_DATA:/data/ -t esfmri python -m esfmri_connectivity.preprocessing.quality_control.find_bad_runs`

#### Create the good voxel masks

`docker run -u esfmri -v $(pwd):/home/esfmri/ -v $ESFMRI_DATA:/data/ -t esfmri python -m esfmri_connectivity.preprocessing.goodvoxel_masks.create_avgvoxdist`

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.preprocessing.goodvoxel_masks.plot_gmm`

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.preprocessing.goodvoxel_masks.create_mask`

### Extract time series

`docker run -u esfmri -v $(pwd):/home/esfmri/ -v $ESFMRI_DATA:/data/ -t esfmri python -m esfmri_connectivity.preprocessing.extract_timeseries.extract_timeseries`

### Community detection

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.communitydetection.run_communitydetection`

### Find stimualtion sites/parcels

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.stimulation_sites.find_stimulation_parcel`

### Analysis 1

`docker run -u esfmri -v $(pwd):/home/esfmri/ -v $ESFMRI_DATA:/data/  -t esfmri python -m esfmri_connectivity.analysis1.calc_fc`

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.analysis1.contrast_and_plot`



