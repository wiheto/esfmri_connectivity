# Fmridenoise preprocessing

## Input data

This step is run after running [fMRIPrep](https://github.com/wiheto/esfmri_connectivity/tree/master/preprocessing/fmriprep)

## Code usage

The fmriprep code used is a slightly modified version of 0.1.1 which is Downloaded in the docker file. The code is [here](https://github.com/wiheto/fmridenoise/tree/9a858744909e919f61c1942df411aeb30c2190e9)

**Step 1**, either run in docker image or convert to singularity.  To fully replicate our steps, a singularity image is needed. Run the following bash code:

```bash
fdnpath=$(pwd)
docker build ./ -t fmridenoise_dev
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $fdnpath/:/output --privileged -t --rm quay.io/singularity/docker2singularity fmridenoise_dev
```

This will export a singularity image into your current directory.

**Step 2**, configure the information in tasks_list.sh. At present it says:

`singularity exec /home/users/wiltho/singularity/fmridenoise_dev* fmridenoise /scratch/users/wiltho/data/esfmri/ --low-pass 0.1 --MultiProc --derivatives fmriprep-1.5.1/fmriprep -w /scratch/users/wiltho/data/esfmri/work`

You will need to change to:

`singularity exec <path-to-singulatiry-image> fmridenoise <bids-directory> --low-pass 0.1 --MultiProc --derivatives <fmriprep-relative-directory> -w <work-directory>`

1.  _path-to-singulatiry-image_: The container command if using docker instead of singularity and the path to the image.
2.  _bids-directory_: The path to the BIDs directory
3.  _fmriprep-relative-directory_: The relative path from bids-directory to the fmriprep derivatives.
4.  _work-directory_: The working directory where fmridenoise stores temporary steps.

**Step 3**, run `task_lists.sh` in the container. This was done on slurm for us, some changes in the `slurm` file will be needed for you (e.g. email, which queue to use etc). Then run:

`sbatch slurm`

If not using slurm, `task_lists.sh` can just be run in bash (and in the singularity image to replicate).

## Output

The output of these steps is that derivatives/fmridenoise has been created with multiple denoising strategies to choose from.
