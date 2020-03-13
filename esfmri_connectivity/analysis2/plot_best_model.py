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
    index = ['median', '% > 0', '% < 0', 'CI[' + str(credrange) + ']']
    df_summary = pd.Series(data=[smap, conf_abovezero, conf_belowzero, [ci_low, ci_high]], index=index)
    return df_summary

def zify(x):
    return (x - np.mean(x)) / np.std(x)

x_vars_1 = ['disp_med_pc_in', 'disp_med_pc_out', 'disp_med_z_in', 'disp_med_z_out']
x_vars_2 = list(itertools.combinations(x_vars_1, 2))
x_vars_3 = list(itertools.combinations(x_vars_1, 3))
x_vars_4 = list(itertools.combinations(x_vars_1, 4))

x_vars_list = x_vars_1 + x_vars_2 + x_vars_3 + x_vars_4

# the best model is PC_in+PC_out, it was model 4 in x_var_list
mi = 4
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
        xstr += s.split('med_')[1]

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
    for n in range(len(betas)):
        y_est += betas[n] * x[n]
    y_like = pm.Normal('y_like', mu=y_est, sd=eps, observed=y)


trace = pm.load_trace('./esfmri_connectivity/analysis2/data/traces/' + df.index[0], model)

# Plot the trace information

fig,ax = plt.subplots(2,2)
ax = ax.flatten()
ax[0].scatter(x[0], y, color='cornflowerblue', s=10)
pd.Series(trace['b0_M' + str(mi)]).plot(kind='density', ax=ax[1], color='cornflowerblue', xlim=[-1, 1])
ax[2].scatter(x[1], y, color='cornflowerblue', s=10)
pd.Series(trace['b1_M' + str(mi)]).plot(kind='density', ax=ax[3], color='cornflowerblue', xlim=[-1, 1])

ax[1].set_ylabel('')
ax[3].set_ylabel('')
ax[1].set_xticks([-1, 0, 1])
ax[3].set_xticks([-1, 0, 1])

plotje.styler(ax[0], aspectsquare=True, xlabel='Displacement PC-within (z)', ylabel='PC stimulation site (z)')
plotje.styler(ax[1], leftaxis='off', xlabel=r'$\beta$', aspectsquare=True, title='Posterior\n(Disp PC-within)')
plotje.styler(ax[2], aspectsquare=True, xlabel='Displacement PC-outside (z)', ylabel='PC stimulation site (z)')
plotje.styler(ax[3], leftaxis='off', xlabel=r'$\beta$', aspectsquare=True, title='Posterior\n(Disp PC-outside)')

pcw_trace_summary = get_trace_stats(trace['b0_M' + str(mi)])
pco_trace_summary = get_trace_stats(trace['b1_M' + str(mi)])

# Add information about posteriors

ax[1].text(0.1, 2, 'Median: ' + str(pcw_trace_summary['median']), fontname='Montserrat', color='gray')
ax[1].text(0.1, 1.4, 'CI: ' + str(pcw_trace_summary['CI[90]']), fontname='Montserrat', color='gray')
ax[1].text(0.1, 1.7, str(pcw_trace_summary['% < 0']) + '% < 0', fontname='Montserrat', color='gray')

ax[3].text(-1.5, 2, 'Median: ' + str(pco_trace_summary['median']), fontname='Montserrat', color='gray')
ax[3].text(-1.5, 1.4, 'CI: ' + str(pco_trace_summary['CI[90]']), fontname='Montserrat', color='gray')
ax[3].text(-1.5, 1.7, str(pco_trace_summary['% > 0']) + '% > 0', fontname='Montserrat', color='gray')

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
