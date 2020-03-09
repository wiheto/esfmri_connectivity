
First run `calc_fc.py` by calling:

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.analysis1.calc_fc`

As stated at numerous other places, when loading raw data, since this loads was done within a singularity container due to mounting issues.