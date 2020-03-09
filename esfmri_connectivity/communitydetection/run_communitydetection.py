import igraph as ig
import leidenalg
import numpy as np
import pandas as pd
from esfmri_connectivity.utils.getfiles import get_timeseries
from sklearn.metrics import adjusted_mutual_info_score
from plotje import styler
import matplotlib.pyplot as plt

save_path = './esfmri_connectivity/communitydetection/'

# Grab data for each subject/task and load
files, savelabels = get_timeseries(group='subtask')
chosen_resolution = []
for fi, filecol in enumerate(files):
    ts = []
    for f in filecol:
        ts.append(pd.read_csv(f, index_col=[0], sep='\t').transpose())
    # Make pearson correlations over all runs for each subject/task
    ts = pd.concat(ts)
    ts.reset_index(inplace=True, drop=True)
    parcel_indices = ts.columns
    # Make connectivity matrices
    g = ts.corr().values
    # Make igrpah variable, make negative connections 0
    g[g < 0] = 0
    G = ig.Graph.Adjacency((g != 0).tolist())
    G.es['weight'] = g[g != 0]
    G.vs['label'] = list(ts.index)
    # Load template and turn names of cortex into community vector
    template = pd.read_csv(
        'esfmri_connectivity/parcellation/tpl-MNI152NLin2009cAsym_res-01_atlas-smorgasbord_dseg.tsv', sep='\t', index_col=[0])
    cortex = template[template.index <= 400]
    namelist = {}
    template_community = []
    for c in cortex['name']:
        name = c.split('_')[2]
        if name not in namelist.keys():
            namelist[name] = len(namelist.keys()) + 1
        template_community.append(namelist[name])
    template_community = np.array(template_community)
    template_community = template_community[(
        ts.transpose().index[ts.transpose().index <= 400])-1]
    # Search through parameter space and run leiden alg. Calculate the AMI with the template
    scores = []
    searchspace = np.arange(0.5, 2.51, 0.01)
    for r in searchspace:
        part = leidenalg.find_partition(G, leidenalg.RBConfigurationVertexPartition, **{
                                        'resolution_parameter': r, 'n_iterations': -1, 'seed': 2019})
        g = ts.transpose().corr().values
        cortex_part = np.array(part.membership)
        cortex_part = cortex_part[:len(
            ts.transpose().index[ts.transpose().index <= 400])]
        scores.append(adjusted_mutual_info_score(
            template_community, cortex_part))
    # Plot the AMI
    fig, ax = plt.subplots(1)
    ax.plot(searchspace, scores)
    styler(ax, ylabel='AMI', xlabel='resolution')
    fig.savefig(save_path + 'ami_figures/' +
                savelabels[fi] + '_ami.png', r=300)
    # Get best score, rerun and save
    best_score = np.argmax(scores)
    r = searchspace[best_score]
    part = leidenalg.find_partition(G, leidenalg.RBConfigurationVertexPartition, **{
                                    'resolution_parameter': r, 'n_iterations': -1, 'seed': 2019})
    df = pd.DataFrame(data={'communities': part.membership}, index=parcel_indices)
    df.to_csv(save_path + 'data/' +  savelabels[fi] + '_communities.tsv', sep='\t')
    chosen_resolution.append(r)

df = pd.DataFrame(data={'subtask': savelabels, 'resolution': chosen_resolution})
df.to_csv(save_path + 'best_resolution_parameters.tsv', sep='\t')