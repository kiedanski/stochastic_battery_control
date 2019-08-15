import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import glob
from constants import *

flist = glob.glob(TMPDIR + 'simplesim*')

pb = POWERWALL2['pb']
ps = POWERWALL2['ps']

res = {}
for fl in flist:
    with open(fl, 'rb') as fh: r = pickle.load(fh)
    if len(r) > 0:
        simnum = fl.split('/')[-1].split('_')[0][9:]
        scennum = fl.split('/')[-1].split('_')[1][:-4]
        if simnum in res:
            res[simnum][scennum] = r
        else:
            res[simnum] = {scennum: r}


def get_real_values(x):
    r = {}
    for k, v in x.items():
        obj = v['3'][1]['obj']
        r[k] = obj
    return r

def get_donth(x):
    r = {}
    for k, v in x.items():
        cons = v['3'][0]
        price = 0
        for i in range(48):
            c = cons[i]
            if c > 0:
                price += c * pb[i]
            else:
                price += c * ps[i]
        r[k] = price
    return r

def get_mpcs(x):
    mpc = {}
    smpc = {}
    smpc2 = {}
    for k, v in x.items():
        mpc_ = np.zeros(len(v))
        smpc_ = np.zeros(len(v))
        smpc2_ = np.zeros(len(v))

        for k1, v1 in v.items():
           mpc_[int(k1) - 3] = v1[5]
           smpc_[int(k1) - 3] = v1[6]
           smpc2_[int(k1) - 3] = v1[7]

        mpc[k] = mpc_
        smpc[k] = smpc_
        smpc2[k] = smpc2_
    return mpc, smpc, smpc2


def plot_objectives(res):
    real = get_real_values(res)
    donth = get_donth(res)
    mpc, smpc, smpc2 = get_mpcs(res)
    subplots_names = ['A', 'B', 'C', 'D']
    x = range(2, 14)
    fig, ax = plt.subplots(2, 2, sharex = True)
    for i in range(4):
        k = str(i + 1)
        ax_ =  ax[i // 2, i % 2]
        ax_.plot(x, mpc[k], 'b*-', label='MPC')
        ax_.plot(x, smpc[k], 'k+-', label='SMPC')
        ax_.plot(x, smpc2[k], 'co-', label='SMPC 14')
        ax_.axhline(y=real[k], c='g', label='Perfect Information')
        ax_.axhline(y=donth[k], c='r', label='No battery')
        ax_.set_title('Case ' + subplots_names[i])
    handles, labels = ax[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=5)
    #fig.tight_layout()
    fig.savefig(IMGDIR + 'objall.pdf')
    return fig, ax

plot_objectives(res)
