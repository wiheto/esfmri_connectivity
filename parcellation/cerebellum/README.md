# Cerebellum atlas

## Attribution and licence of the cerebellum atlas

Attribution for this atlas: King, M., Hernandez-Castillo, C.R., Poldrack, R. Ivry, R., Diedrichsen, J. (2019). [Functional boundaries in the human cerebellum revealed by a multi-domain task battery](https://www.nature.com/articles/s41593-019-0436-x). Nature Neuroscience.

The SUIT atlas files are shared under the [Creative Commons Attribution-NonCommercial 3.0 Unported License](http://creativecommons.org/licenses/by-nc/3.0/deed.en_US) and this licence applies to them here. Read more info [here](http://www.diedrichsenlab.org/imaging/mdtb.htm)

## How to recreate the files in this repo

All the files that are needed in this project are provided in this repo.

## Step 1: Download the file

The file mdtb.zip was downloaded from [here](http://www.diedrichsenlab.org/imaging/mdtb.htm). In the zip file `/website_maps/Parcellation/MNI_MDTB_10Regions.nii` was exported to this directory.

## Step 2: Compress

In this directory type in terminal: `gzip ./parcellation/cerebellum/MNI_MDTB_10Regions.nii`. This will create a .nii.gz file (what is included in the directory here)

## Step 3: Create templateflow name

Create a filename compatible with templateflow's naming structure:

`cp ./parcellation/cerebellum/MNI_MDTB_10Regions.nii.gz ./parcellation/cerebellum/tpl-MNI152NLin6Asym_res-01_atlas-King2019Cerebellum_dseg.nii.gz`

## Step 4: Create metadata

The file:

`./parcellation/cerebellum/tpl-MNI152NLin6Asym_res-01_atlas-King2019Cerebellum_dseg.tsv`

Was created manually using the information in the above cited article, and [this figure](http://www.diedrichsenlab.org/imaging/Pics/MDTB_parcellation.png). It contains the meta information for the different ROIs.

## Step 5: convert to MNI152NLin2009cAsym

Run the python script in a docker container. Make sure you are in the main directory of this repo.

```bash
docker build ./ -t esfmri
docker run -u `id -u` -v $(pwd):/home/esfmri/ -t esfmri python parcellation/cerebellum/reref_fromfsl_to_mni2009c.py
```

This will create the file: `./parcellation/cerebellum/tpl-MNI152NLin2009cAsym_res-01_atlas-King2019Cerebellum_dseg.nii.gz`

Finally, copy the metadata from MNI152NLin6Asym to MNI152NLin2009cAsym. It is the same information, but good to update the tpl key/value pair:

`cp tpl-MNI152NLin6Asym_res-01_atlas-King2019Cerebellum_dseg.tsv tpl-MNI152NLin2009cAsym_res-01_atlas-King2019Cerebellum_dseg.tsv`
