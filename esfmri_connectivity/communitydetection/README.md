# Community detection

Community detection was done with the Leiden algorithem ([Traag et al 2018](https://arxiv.org/abs/1810.084730)) using Reichardt & Bornholdt ([2006](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.74.016110)) null model (RBConfigurationVertexPartition). Only positive edges used. The resolution parameter was determined based on the adjusted multual information between the cortical parcels and the Yeo 7 network template ([Yeo et al 2012](https://www.physiology.org/doi/abs/10.1152/jn.00338.2011)).

## Contents of directory

__run_communitydetection.py__ creates all the contents of this directory.
__best_resolution_parametrs.tsv__ tabular file containing all the largest adjusted mutual information value for each subtask combination.
__./ami_figures__ contains the adjusted mutual information for each subtask combination for different settings of the resolution parameter.
__./data__ contains the community partition of each subtask.

## To replicate

``docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.communitydetection.run_communitydetection``
