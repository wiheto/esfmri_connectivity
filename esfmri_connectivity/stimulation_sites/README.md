# Stimulation sites

The stimulation site coordinates consisted of two channels (A and B). A got the leading positive phase of stimulation.
We decided to make stimulation sites equidistant between the two channels. We placed a 3mm ROI on the at this coordinate. We then checked which parcels overlapped the most with it.

The stimulation_information tsv files can be considered part of the raw data should be packaged with raw data at release (how they will be included at release is unclear at time of writing, so they are included here for reproducibility purposes). The stimulation sites in 2009c have been converted from Nlin6 using TemplateFlow and ants.

Prior to running the next step, the time series should be derived.

The file `stimsite2parcel.tsv` is created by running the `find_stimulation_parcels.tsv`. To replicate the step, run:

`docker run -u esfmri -v $(pwd):/home/esfmri/ -t esfmri python -m esfmri_connectivity.stimulation_sites.find_stimulation_parcel`
