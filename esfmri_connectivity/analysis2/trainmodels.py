import pandas as pd
import pymc3 as pm
import arviz
import numpy as np
import itertools

df_cp = pd.read_csv('./esfmri_connectivity/analysis1/data/cartprofile/cartprofile_displacement.tsv', sep='\t', index_col=[0])
df_stim = pd.read_csv('./esfmri_connectivity/analysis2/data/pc_at_stimsite.tsv', sep='\t', index_col=[0])

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


trace_dict = {}
for mi, x_vars in enumerate(x_vars_list):
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
            # xstr += s.split('med_')[1]
            xstr += s
    else:
        tmp = df_cp[x_vars].values
        x.append(zify(tmp))
        # xstr += x_vars.split('med_')[1]
        xstr += x_vars

    with pm.Model():
        a = pm.Cauchy('a_M' + str(mi), alpha=0, beta=1)
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
            y_est += beta * x[n]

        y_like = pm.Normal('y_like', mu=y_est, sd=eps, observed=y)

        traces = pm.sample(draws=10000, tune=1000, chains=2, random_seed=2020)
        pm.save_trace(traces, './esfmri_connectivity/analysis2/data/traces/' + xstr, overwrite=True)

    trace_dict[xstr] = traces


mi = 'C'
xstr = 'control'
with pm.Model():
    a = pm.Cauchy('a_M' + str(mi), alpha=0, beta=1)
    eps = pm.HalfCauchy('eps', beta=5)

    # Expected value
    y_est = a

    y_like = pm.Normal('y_like', mu=y_est, sd=eps, observed=y)

    traces = pm.sample(draws=10000, tune=1000, chains=2, random_seed=2020)
    pm.save_trace(traces, './esfmri_connectivity/analysis2/data/traces/' + xstr, overwrite=True)

trace_dict[xstr] = traces


loo_results = arviz.compare(trace_dict, 'loo')
waic_results = arviz.compare(trace_dict, 'waic')

loo_results.to_csv('./esfmri_connectivity/analysis2/data/model_fit_loo.tsv', sep='\t')
waic_results.to_csv('./esfmri_connectivity/analysis2/data/model_fit_waic.tsv', sep='\t')
