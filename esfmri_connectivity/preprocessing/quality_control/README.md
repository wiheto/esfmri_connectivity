## Quality control 

### Input data

Raw data needs to be downloaded from openneuro.org. And preprocessed with fmriprep and fmridenoise.

### Contents

__fmriprep_evaluation.tsv__: this is a subjective evaluation of the reports. 
__fmridenoise_failures.tsv__: these are the files that failed to run in fmridenoise due to the length of file being too small. They are all already flagged in fmriprep_evaluation. However, to get the then current version of fmridenoise to complete, these runs have to be deleted from the fmriprep derivative output.  
__bad_runs.tsv__: A list of the bad runs where the average framewise displacement was greater than 0.5.
__find_bad_runs.py__: Script to create the file bad_runs.tsv.