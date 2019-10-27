# Fmridenoise preprocessing

## Input data

This step is run after running [fMRIPrep](https://github.com/wiheto/esfmri_connectivity/tree/master/preprocessing/fmriprep)

## Code useage 

__Step 1__, in this directory run:

`git clone https://github.com/wiheto/fmridenoise/tree/add_workdir`

This is the specific version of fmriprep denoise used (slightly modified version of 0.1.1). 

__Step 2__, either run in docker image or convert to sinularity (the next step uses a singularity image). The second step is only needed if running singularity: 

```
fdnpath=$(pwd)
docker build ./ -t fmridenoise_dev
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $fdnpath/:/output --privileged -t --rm quay.io/singularity/docker2singularity fmridenoise_dev
```

This will export a singularity image into your current directory.

__Step 3__, configure the informatoin in tasks_list.sh. At present it says: 

`singularity exec /home/users/wiltho/singularity/fmridenoise_dev* fmridenoise /scratch/users/wiltho/data/esfmri/ --low-pass 0.1 --MultiProc --derivatives fmriprep-1.5.1/fmriprep -w /scratch/users/wiltho/data/esfmri/work`

You will need to change: 

1. The container command if using docker instead of singularity and the path to the image.  
2. The path to the BIDs directory (path following fmridenoise and before --low-pass)
3. The derivatives relative path (after --derivatives) in the BIDs directory to fmriprep if not ./fmriprep-1.5.1/fmriprep
4. THe working directory (after -w flag) where fmridenoise stores temporary steps.     

__Step 4__, run `task_lists.sh` in the container. This was done on slurm for us, some changes in the slurm file will be needed for you (e.g. email, which queue to use etc). Then run:

`sbatch slurm`   

If not using slurm, this can just be run in bash instead. 

## Output

The output of these steps is that derivatives/fmridenoise has been created with multiple denoising strategies to choose from.
