# Analysis 1

Analysis 1 compares whether the stimulation site's community has greater displacement (i.e. es-on vs es-off) of the participation coefficient and within module degree z-score compared to other communities. This is quantified by looking at the max and median of both network theory measures.

Summary of positive results: the median PC of the stimulation site's community increases when stimulation is on compared to stimulation is off. This difference was, on average, significantly greater than outside the stimulation community (p<0.05 Bonferroni corrected).

All other comparisons confirmed the null hypothesis that there was no difference between stimulation community and outside its community.

## Replication and description of directory contents

First run `calc_fc.py` by calling:

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.analysis1.calc_fc`

The above code needs to read the BIDS raw directory to get the events file. As stated at numerous other places, when we ran this step, we did it through a singularity container instead due to the BIDS raw directory being mounted from an external source.

Next, we ran `contrast_and_plot.py` by running (this time with the Docker container):

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.analysis1.contrast_and_plot`

This performs the statistical analysis for "analysis 1", and saves the output to `stats` and `figures`.

In figures, there is an SVG and PNG file summarizing the results (`cartprofile_displacement`). In stats, there are two tsv files. One is a `summary.tsv` of the statistical tests performed. The second is the non-parametric distributions generated for the statistical testing (`nonparametric_permuted_distributions.tsv`).
