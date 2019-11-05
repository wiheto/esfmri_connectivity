from plotje import styler
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import os


def plot_fitted_gm(data, predicted_gm, ax=None, points=10000, plot_resolution=100, plot_threshold=True, title=None):
    """
    Function plots the predicted class of the GMM model 
    """
    if title is None:
        title = ''
    if ax is None:
        _, ax = plt.subplots(1, 1)
    xs = np.linspace(data.min(), data.max(), plot_resolution)
    for n in np.unique(predicted_gm):
        ax.hist(data[predicted_gm == n], bins=xs, alpha=0.5)
    ax.set_xlim([data.min(), data.max()])
    styler(ax, leftaxis='off', title=title)
    return ax


rel_dir = './esfmri_connectivity/preprocessing/goodvoxel_masks/avg_voxel_distribution/'
files = os.listdir(rel_dir)
files = [f for f in files if f.endswith('_voxdist.npy')]
for f in files:
    # if not os.path.exists(rel_dir + 'gmm_figures/' + f.split('_voxdist')[0] + '_hist.png'):
    print(f)
    data = np.load(rel_dir + f)
    data = np.array(data, ndmin=2).transpose()
    fig, ax = plt.subplots(1, 5, figsize=(8, 2))
    ax = ax.flatten()
    for c in range(1, 6):
        fitted_gm = GaussianMixture(c, random_state=2019)
        fitted_gm.fit(data)
        predicted_gm = fitted_gm.predict(data)
        plot_fitted_gm(data, predicted_gm, plot_resolution=100,
                       ax=ax[c-1], title=c)

    fig.tight_layout()
    fig.savefig(rel_dir + 'gmm_figures/' +
                f.split('_voxdist')[0] + '_hist.png', r=300)
