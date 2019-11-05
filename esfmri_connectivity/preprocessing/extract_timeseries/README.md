# Extract timeseries. 

The output of this code it to create time series in ./esfmri_connectivity/timeseries/. Two different types of time series are created. The first, time-points are as is. The second have the `desc-fdcensored` in the name and these have nan values for the time-points that are above 0.5 in framewise displacement.

## Replicating steps

If replicating code, you must first make sure that all the code in `preprocessing/goodvoxel_masks` has been performed.

Check lines 7-13 to make sure the different directory names match what you have.

After that, run `perform_parcellation.py` in a container. Here we ran it interactively in a singularity container following the instructions that exist in `preprocessing/goodvoxel_masks`.

Again, this can be run with docker run command and mounting two directories. This would mean that the following will work (when paths are correctly specified): `docker run -u esfmri -v $(pwd):/home/esfmri/ -v path-to-bids-dir:path-specified-in-line-7 -t esfmri python -m esfmri_connectivity.preprocessing.extract_timeseries.extract_timeseries ` The reason why we ran it in a singularity container was because the bids_dir was remotely mounted which cannot be mounted as above and would require additional changes to the Dockerfile.

