#!/bin/sh
singularity exec /home/users/wiltho/singularity/fmridenoise_dev-2019-10-26* fmridenoise /scratch/users/wiltho/data/esfmri/ --low-pass 0.1 --MultiProc --derivatives fmriprep-1.5.1/fmriprep -w /scratch/users/wiltho/data/esfmri/work
