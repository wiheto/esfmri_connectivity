import matplotlib.pyplot as plt
import pandas as pd
import plotje
import pymc3 as pm
import numpy as np
import itertools

df = pd.read_csv('./esfmri_connectivity/analysis2/data/model_fit_loo.tsv', sep='\t', index_col=[0])
df_cp = pd.read_csv('./esfmri_connectivity/analysis1/data/cartprofile/cartprofile_displacement.tsv', sep='\t', index_col=[0])
df_stim = pd.read_csv('./esfmri_connectivity/analysis2/data/pc_at_stimsite.tsv', sep='\t', index_col=[0])


def iqr(x, a=0):
    return np.subtract(*np.percentile(x, [75, 25], axis=a))


def get_trace_stats(trace, credrange=90):
    # credrange at 90%
    # Get indicies at 5 and 95%
    ilow = trace.shape[0]*np.round((1 - (credrange / 100)) / 2, 2)
    ihigh = trace.shape[0]*(1 - np.round((1 - (credrange / 100)) / 2, 2))
    # Perfentage above/below 0
    conf_abovezero = np.round(sum(trace > 0) / trace.shape[0] * 100, 1)
    conf_belowzero = np.round(sum(trace < 0) / trace.shape[0] * 100, 1)
    # median
    smap = np.round(np.median(trace), 2)
    # credible interval low and high
    ci_low = np.round(np.sort(trace)[int(ilow)], 2)
    ci_high = np.round(np.sort(trace)[int(ihigh)], 2)

    tmin = np.min(trace)
    tmax = np.max(trace)

    index = ['median', '% > 0', '% < 0', 'CI[' + str(credrange) + ']', 'minmax']
    df_summary = pd.Series(data=[smap, conf_abovezero, conf_belowzero, [ci_low, ci_high], [tmin, tmax]], index=index)
    return df_summary

def zify(x):
    return (x - np.mean(x)) / np.std(x)


x_vars_1 = ['disp_med_pc_in', 'disp_med_pc_out', 'disp_med_z_in', 'disp_med_z_out', 'disp_max_pc_in', 'disp_max_pc_out', 'disp_max_z_in', 'disp_max_z_out']
x_vars_2 = list(itertools.combinations(x_vars_1, 2))
x_vars_3 = list(itertools.combinations(x_vars_1, 3))
x_vars_4 = list(itertools.combinations(x_vars_1, 4))
x_vars_5 = list(itertools.combinations(x_vars_1, 5))
x_vars_6 = list(itertools.combinations(x_vars_1, 6))
x_vars_7 = list(itertools.combinations(x_vars_1, 7))
x_vars_8 = list(itertools.combinations(x_vars_1, 8))

x_vars_list = x_vars_1 + x_vars_2 + x_vars_3 + x_vars_4 + x_vars_5 + x_vars_6 + x_vars_7 + x_vars_8

# the best model is med-PC_in+med-PC_out+max-z-out, it was model 41 in x_var_list
mi = 41
# recreate model
x_vars = x_vars_list[mi]
y = np.array(df_stim['PC'].values)
y = zify(y)

x = []
xstr = ''
if isinstance(x_vars, tuple):
    for i, s in enumerate(x_vars):
        tmp = df_cp[s].values
        x.append(zify(tmp))
        if i > 0:
            xstr += '+'
        xstr += s
else: 
    tmp = df_cp[x_vars].values
    x.append(zify(tmp))

with pm.Model() as model:
    # Intercept for each county, distributed around group mean mu_a
    a = pm.Cauchy('a_M' + str(mi), alpha=0, beta=1)
    # Intercept for each county, distributed around group mean mu_a
    betas = []
    if isinstance(x_vars, tuple):
        for i, n in enumerate(range(len(x_vars))):
            betas.append(pm.Cauchy('b' + str(i) + '_M' + str(mi), alpha=0, beta=1))
    else:
        betas.append(pm.Cauchy('b0_M' + str(mi), alpha=0, beta=1))
    print(betas)
    eps = pm.HalfCauchy('eps', beta=5)
    # Expected value
    y_est = a
    for n, beta in enumerate(betas):
        y_est += betas[n] * x[n]
    y_like = pm.Normal('y_like', mu=y_est, sd=eps, observed=y)

trace = pm.load_trace('./esfmri_connectivity/analysis2/data/traces/' + df.index[0], model)

# Plot the trace information
pcw_trace_summary = get_trace_stats(trace['b0_M' + str(mi)])
pco_trace_summary = get_trace_stats(trace['b1_M' + str(mi)])
zo_trace_summary = get_trace_stats(trace['b2_M' + str(mi)])
intercept_trace_summary = get_trace_stats(trace['a_M' + str(mi)])


fig,ax = plt.subplots(2,2, figsize=(8,8))
gs = ax[1,1].get_gridspec()
ax = ax.flatten()

xline = np.arange(-3,3,0.25)
yline = np.arange(-3,3,0.25) * pcw_trace_summary['median']
ax[0].plot(xline, yline, color='black')
ax[0].plot(xline, xline*pcw_trace_summary['CI[90]'][0], '--', alpha=0.5, color='black')
ax[0].plot(xline, xline*pcw_trace_summary['CI[90]'][1], '--', alpha=0.5, color='black')
ax[0].scatter(x[0], y, color='gray', s=20)

xline = np.arange(-3,3,0.25)
yline = np.arange(-3,3,0.25) * pco_trace_summary['median']
ax[1].plot(xline, yline, color='black')
ax[1].plot(xline, xline*pco_trace_summary['CI[90]'][0], '--', alpha=0.5, color='black')
ax[1].plot(xline, xline*pco_trace_summary['CI[90]'][1], '--', alpha=0.5, color='black')
ax[1].scatter(x[1], y, color='gray', s=20)

xline = np.arange(-3,3,0.25)
yline = np.arange(-3,3,0.25) * zo_trace_summary['median']
ax[2].plot(xline, yline, color='black')
ax[2].plot(xline, xline*zo_trace_summary['CI[90]'][0], '--', alpha=0.5, color='black')
ax[2].plot(xline, xline*zo_trace_summary['CI[90]'][1], '--', alpha=0.5, color='black')
ax[2].scatter(x[2], y, color='gray', s=20)

ax[0].set_xlim([-3.2, 3.2])
ax[0].set_ylim([-3.2, 3.2])
ax[1].set_xlim([-3.2, 3.2])
ax[1].set_ylim([-3.2, 3.2])
ax[2].set_xlim([-3.2, 3.2])
ax[2].set_ylim([-3.2, 3.2])


plotje.styler(ax[0], aspectsquare=True, xlabel=r'median $PC_{within}$ (z-scored)', ylabel='PC stimulation site (z-scored)')
plotje.styler(ax[1], aspectsquare=True, xlabel=r'median $PC_{outside}$ (z-scored)', ylabel='PC stimulation site (z-scored)')
plotje.styler(ax[2], aspectsquare=True, xlabel=r'max $z_{outside}$ (z-scored)', ylabel='PC stimulation site (z-scored)')

ax[0].set_yticks(np.arange(-3, 3.1))
ax[0].set_xticks(np.arange(-3, 3.1))
ax[1].set_yticks(np.arange(-3, 3.1))
ax[1].set_xticks(np.arange(-3, 3.1))
ax[2].set_yticks(np.arange(-3, 3.1))
ax[2].set_xticks(np.arange(-3, 3.1))
ax[0].set_yticklabels(np.arange(-3, 3.1))
ax[0].set_xticklabels(np.arange(-3, 3.1))
ax[1].set_yticklabels(np.arange(-3, 3.1))
ax[1].set_xticklabels(np.arange(-3, 3.1))
ax[2].set_yticklabels(np.arange(-3, 3.1))
ax[2].set_xticklabels(np.arange(-3, 3.1))


ax[3].scatter(pco_trace_summary['minmax'], [2,2], s=3, color='gray')
ax[3].scatter(pcw_trace_summary['minmax'], [1,1], s=3, color='gray')
ax[3].scatter(intercept_trace_summary['minmax'], [4,4], s=3, color='gray')
ax[3].scatter(zo_trace_summary['minmax'], [3,3], s=3, color='gray')


ax[3].scatter(pco_trace_summary['median'], [2], marker='s', s=20, zorder=50, color='black')
ax[3].scatter(pcw_trace_summary['median'], [1], marker='s', s=20, zorder=50, color='black')
ax[3].scatter(intercept_trace_summary['median'], [4], marker='s', s=20, zorder=50, color='black')
ax[3].scatter(zo_trace_summary['median'], [3], marker='s', s=20, zorder=50, color='black')


ax[3].plot(pco_trace_summary['CI[90]'], [2,2], color='gray', linewidth=1)
ax[3].plot(pcw_trace_summary['CI[90]'], [1,1], color='gray', linewidth=1)
ax[3].plot(intercept_trace_summary['CI[90]'], [4,4], color='gray', linewidth=1)
ax[3].plot(zo_trace_summary['CI[90]'], [3,3], color='gray', linewidth=1)

plotje.styler(ax[3], aspectsquare=True, xlabel='Posterior distribution')

ax[3].set_yticks([1, 2, 3, 4])
ax[3].set_yticklabels([r'median $PC_{within}$', r'median $PC_{outside}$', r'max $z_{outside}$', 'intercept'])
ax[3].set_xticks([-1, -0.5, 0, 0.5, 1])
ax[3].set_xticklabels([-1, -0.5, 0, 0.5, 1])
fig.tight_layout()


fig.savefig('./esfmri_connectivity/analysis2/figures/posterior.svg')
fig.savefig('./esfmri_connectivity/analysis2/figures/posterior.png', r=600)




# ppc checks

ppc = pm.sample_posterior_predictive(trace, model=model, samples=10000, random_seed=2020)
ppc_mean = np.mean(ppc['y_like'],1)
y_mean = np.mean(y)
ppc_iqr = iqr(ppc['y_like'],1)
y_iqr = iqr(y)
ppc_mean_p = np.mean(ppc_mean >= y_mean)
ppc_iqr_p = np.mean(ppc_iqr >= y_iqr)
ppc = pd.Series(data={'p_mean': ppc_mean_p, 'q_iqr': ppc_iqr_p})
ppc.to_csv('./esfmri_connectivity/analysis2/data/ppc_bestmodel.tsv', sep='\t')

# Gelam rubin statistic
gr = pd.Series(pm.gelman_rubin(trace))
gr.to_csv('./esfmri_connectivity/analysis2/data/gelmanrubin_bestmodel.tsv', sep='\t')
